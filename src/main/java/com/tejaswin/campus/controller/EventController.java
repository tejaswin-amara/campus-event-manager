package com.tejaswin.campus.controller;

import com.tejaswin.campus.model.Event;
import com.tejaswin.campus.model.User;
import com.tejaswin.campus.service.EventService;
import com.tejaswin.campus.service.SessionService;
import com.tejaswin.campus.security.SecurityAuditLogger;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Controller
@RequestMapping("/student")
public class EventController {

    private static final Logger logger = LoggerFactory.getLogger(EventController.class);

    private final EventService eventService;
    private final SessionService sessionService;
    private final SecurityAuditLogger auditLogger;

    public EventController(EventService eventService, SessionService sessionService, SecurityAuditLogger auditLogger) {
        this.eventService = eventService;
        this.sessionService = sessionService;
        this.auditLogger = auditLogger;
    }

    @GetMapping("/dashboard")
    @Transactional(readOnly = true)
    public String studentDashboard(
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String category,
            Model model) {

        User user = sessionService.getLoggedInUser();
        if (user == null) {
            return "redirect:/";
        }

        List<Event> events;
        if (search != null && !search.trim().isEmpty()) {
            events = eventService.searchEvents(search);
            model.addAttribute("searchQuery", search);
        } else if (category != null && !category.trim().isEmpty() && !"all".equalsIgnoreCase(category)) {
            events = eventService.findEventsByCategory(category);
            model.addAttribute("activeCategory", category);
        } else {
            events = eventService.findAllEvents();
        }

        if (events == null) {
            events = java.util.Collections.emptyList();
        }

        model.addAttribute("events", events);
        model.addAttribute("user", user);
        model.addAttribute("now", java.time.LocalDateTime.now());
        return "dashboard";
    }

    @GetMapping("/register-external/{eventId}")
    @CircuitBreaker(name = "registrationService", fallbackMethod = "registrationFallback")
    @Transactional
    public String registerExternal(@PathVariable(name = "eventId") Long eventId) {
        User user = sessionService.getLoggedInUser();
        if (user == null) {
            return "redirect:/";
        }

        // Track interest for analytics
        auditLogger.logSecurityLinkClick(user.getUsername(), "REGISTER_EXTERNAL", eventId);
        eventService.registerStudent(eventId, user.getId());

        Event event = eventService.findEventById(eventId);
        if (event != null && event.getRegistrationLink() != null && !event.getRegistrationLink().isEmpty()) {

            String link = event.getRegistrationLink().trim();
            // Security: Only allow HTTP/HTTPS redirects to prevent open-redirect attacks
            if (link.startsWith("http://") || link.startsWith("https://")) {
                return "redirect:" + link;
            }
            logger.warn("SECURITY: Blocked redirect to untrusted URL scheme for event {}: {}", eventId, link);
        }

        return "redirect:/student/event/" + eventId;
    }

    public String registrationFallback(Long eventId, Exception e) {
        logger.error("Circuit breaker triggered for registration of event {}: {}", eventId, e.getMessage());
        return "redirect:/student/event/" + eventId + "?error=service_unavailable";
    }

    @GetMapping("/event/{id}")
    public String eventDetail(@PathVariable Long id) {
        if (sessionService.getLoggedInUser() == null) {
            return "redirect:/";
        }
        return "redirect:/student/dashboard?open=" + id;
    }
}
