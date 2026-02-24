package com.tejaswin.campus.controller;

import com.tejaswin.campus.model.Event;
import com.tejaswin.campus.service.EventService;
import com.tejaswin.campus.security.SecurityAuditLogger;
import com.tejaswin.campus.service.SessionService;
import com.tejaswin.campus.exception.EventNotFoundException;
import com.tejaswin.campus.exception.InvalidImageException;
import com.tejaswin.campus.config.AppConfig;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.lang.NonNull;
import org.springframework.transaction.annotation.Transactional;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Set;
import java.util.UUID;

@Controller
@RequestMapping("/admin")
public class AdminController {

    private static final Logger logger = LoggerFactory.getLogger(AdminController.class);
    private static final Set<String> ALLOWED_IMAGE_EXTENSIONS = Set.of(".jpg", ".jpeg", ".png", ".webp", ".gif");

    private final EventService eventService;
    private final SessionService sessionService;
    private final SecurityAuditLogger auditLogger;
    private final Path uploadBaseDir;

    public AdminController(EventService eventService, AppConfig appConfig, SessionService sessionService,
            SecurityAuditLogger auditLogger) {
        this.eventService = eventService;
        this.sessionService = sessionService;
        this.auditLogger = auditLogger;
        this.uploadBaseDir = Paths.get(appConfig.getUploadDir()).toAbsolutePath().normalize();
    }

    @GetMapping("/dashboard")
    @Transactional(readOnly = true)
    public String adminDashboard(Model model) {
        if (!sessionService.isAdmin()) {
            return "redirect:/";
        }

        List<Event> events = eventService.findAllEvents();
        if (events == null)
            events = java.util.Collections.emptyList();

        // Analytics
        model.addAttribute("totalEvents", events.size());

        java.util.Map<String, Long> categoryCounts = eventService.getCategoryCounts();
        if (categoryCounts == null)
            categoryCounts = java.util.Collections.emptyMap();
        model.addAttribute("categoryCounts", categoryCounts);

        Long upcomingEvents = eventService.getUpcomingEventsCount();
        if (upcomingEvents == null)
            upcomingEvents = 0L;
        model.addAttribute("upcomingEvents", upcomingEvents);

        Long pastEvents = eventService.getPastEventsCount();
        if (pastEvents == null)
            pastEvents = 0L;
        model.addAttribute("pastEvents", pastEvents);

        // System Health
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        model.addAttribute("sysMemoryUsed", usedMemory / (1024 * 1024)); // MB
        model.addAttribute("sysMemoryTotal", totalMemory / (1024 * 1024)); // MB
        model.addAttribute("sysCores", runtime.availableProcessors());

        model.addAttribute("events", events);
        model.addAttribute("user", sessionService.getLoggedInUser());
        model.addAttribute("newEvent", new Event());
        model.addAttribute("now", LocalDateTime.now());
        return "admin_dashboard";
    }

    @PostMapping("/add-event")
    @Transactional
    public String addEvent(@RequestParam String title,
            @RequestParam String description,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime dateTime,
            @RequestParam String venue,
            @RequestParam String category,
            @RequestParam(required = false) String registrationLink,
            @RequestParam(required = false) Integer maxCapacity,
            @RequestParam(required = false) MultipartFile imageFile,
            @RequestParam(required = false) String responsesLink,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endDateTime,
            RedirectAttributes redirectAttributes,
            HttpServletRequest request) {

        if (!sessionService.isAdmin()) {
            return "redirect:/";
        }

        if (endDateTime != null && endDateTime.isBefore(dateTime)) {
            redirectAttributes.addFlashAttribute("error", "End date cannot be before start date!");
            return "redirect:/admin/dashboard";
        }

        Path newlyUploadedPath = null;
        try {
            Event event = new Event();
            event.setTitle(title);
            event.setDescription(description);
            event.setDateTime(dateTime);
            event.setVenue(venue);
            event.setCategory(category);
            event.setRegistrationLink(registrationLink);
            event.setMaxCapacity(maxCapacity);
            event.setResponsesLink(responsesLink);
            event.setEndDateTime(endDateTime);

            if (imageFile != null && !imageFile.isEmpty()) {
                String savedUrl = saveUploadedImage(imageFile, sessionService.getLoggedInUser().getUsername());
                if (savedUrl != null) {
                    event.setImageUrl(savedUrl);
                    newlyUploadedPath = uploadBaseDir.resolve(savedUrl.substring("/uploads/".length())).normalize();
                } else {
                    throw new InvalidImageException("Invalid image file. Allowed: JPG, PNG, WebP, GIF.");
                }
            }

            eventService.saveEvent(event);
            redirectAttributes.addFlashAttribute("success", "Event added successfully!");
        } catch (Exception e) {
            // Clean up newly uploaded file if DB save fails
            if (newlyUploadedPath != null) {
                try {
                    Files.deleteIfExists(newlyUploadedPath);
                    logger.warn("AUDIT: Deleted newly uploaded file due to transaction failure in addEvent: {}",
                            newlyUploadedPath);
                } catch (Exception ex) {
                    logger.error("Failed to clean up file after transaction failure in addEvent", ex);
                }
            }
            throw e;
        }
        return "redirect:/admin/dashboard";
    }

    @PostMapping("/edit-event")
    @Transactional
    public String editEvent(@RequestParam Long id,
            @RequestParam String title,
            @RequestParam String description,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime dateTime,
            @RequestParam String venue,
            @RequestParam String category,
            @RequestParam(required = false) String registrationLink,
            @RequestParam(required = false) Integer maxCapacity,
            @RequestParam(required = false) MultipartFile imageFile,
            @RequestParam(required = false) String responsesLink,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endDateTime,
            RedirectAttributes redirectAttributes,
            HttpServletRequest request) {

        if (!sessionService.isAdmin()) {
            return "redirect:/";
        }

        if (endDateTime != null && endDateTime.isBefore(dateTime)) {
            redirectAttributes.addFlashAttribute("error", "End date cannot be before start date!");
            return "redirect:/admin/dashboard";
        }

        Event event = eventService.findEventById(id);
        if (event == null) {
            throw new EventNotFoundException("Event not found with ID: " + id);
        }

        Path newlyUploadedPath = null;
        try {
            event.setTitle(title);
            event.setDescription(description);
            event.setDateTime(dateTime);
            event.setVenue(venue);
            event.setCategory(category);
            event.setRegistrationLink(registrationLink);
            event.setMaxCapacity(maxCapacity);
            event.setResponsesLink(responsesLink);
            event.setEndDateTime(endDateTime);

            if (imageFile != null && !imageFile.isEmpty()) {
                String oldUrl = event.getImageUrl();
                String savedUrl = saveUploadedImage(imageFile, sessionService.getLoggedInUser().getUsername());

                if (savedUrl == null) {
                    throw new InvalidImageException("Invalid image file. Allowed: JPG, PNG, WebP, GIF.");
                }

                event.setImageUrl(savedUrl);
                newlyUploadedPath = uploadBaseDir.resolve(savedUrl.substring("/uploads/".length())).normalize();

                // Delete old image
                if (oldUrl != null && oldUrl.startsWith("/uploads/")) {
                    try {
                        String oldFile = oldUrl.substring("/uploads/".length());
                        Path oldPath = uploadBaseDir.resolve(oldFile).normalize();
                        if (oldPath.startsWith(uploadBaseDir)) {
                            Files.deleteIfExists(oldPath);
                        }
                    } catch (Exception e) {
                        logger.warn("Failed to delete old image file: {}", oldUrl, e);
                    }
                }
            }

            eventService.saveEvent(event);
            redirectAttributes.addFlashAttribute("success", "Event updated successfully!");
        } catch (Exception e) {
            // Clean up newly uploaded file if DB save fails
            if (newlyUploadedPath != null) {
                try {
                    Files.deleteIfExists(newlyUploadedPath);
                    logger.warn("AUDIT: Deleted newly uploaded file due to transaction failure: {}", newlyUploadedPath);
                } catch (Exception ex) {
                    logger.error("Failed to clean up file after transaction failure", ex);
                }
            }
            throw e;
        }
        return "redirect:/admin/dashboard";
    }

    @PostMapping("/delete-event/{id}")
    @Transactional
    public String deleteEvent(@PathVariable @NonNull Long id,
            RedirectAttributes redirectAttributes) {

        if (!sessionService.isAdmin()) {
            return "redirect:/";
        }

        eventService.deleteEvent(id);
        redirectAttributes.addFlashAttribute("success", "Event deleted successfully!");
        return "redirect:/admin/dashboard";
    }

    @GetMapping("/export-events")
    public ResponseEntity<byte[]> exportEvents() {
        if (!sessionService.isAdmin()) {
            return ResponseEntity.status(403).build();
        }

        byte[] csvData = eventService.getAllEventsAsCsv();

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=campus_events_report.csv")
                .header(HttpHeaders.CONTENT_TYPE, "text/csv")
                .body(csvData);
    }

    private String saveUploadedImage(MultipartFile imageFile, String username) {
        String originalFilename = imageFile.getOriginalFilename();
        if (originalFilename == null || originalFilename.isBlank()) {
            return null;
        }

        String sanitizedFilename = originalFilename.replaceAll("[^a-zA-Z0-9._-]", "_");
        String ext = "";
        int i = sanitizedFilename.lastIndexOf('.');
        if (i > 0) {
            ext = sanitizedFilename.substring(i).toLowerCase();
        }

        if (!ALLOWED_IMAGE_EXTENSIONS.contains(ext)) {
            auditLogger.logFileUpload(username, originalFilename, imageFile.getSize(), "REJECTED_INVALID_EXTENSION");
            return null;
        }

        try {
            String fileName = UUID.randomUUID().toString() + ext;
            Path targetPath = uploadBaseDir.resolve(fileName).normalize();

            if (!targetPath.startsWith(uploadBaseDir)) {
                auditLogger.logFileUpload(username, originalFilename, imageFile.getSize(), "REJECTED_PATH_TRAVERSAL");
                return null;
            }

            if (!Files.exists(uploadBaseDir)) {
                Files.createDirectories(uploadBaseDir);
            }

            if (Files.isSymbolicLink(targetPath)) {
                auditLogger.logFileUpload(username, originalFilename, imageFile.getSize(), "REJECTED_SYMLINK");
                return null;
            }

            try (var inputStream = imageFile.getInputStream()) {
                Files.copy(inputStream, targetPath,
                        java.nio.file.StandardCopyOption.REPLACE_EXISTING,
                        java.nio.file.LinkOption.NOFOLLOW_LINKS);
            }
            auditLogger.logFileUpload(username, originalFilename, imageFile.getSize(), "SUCCESS");
            return "/uploads/" + fileName;
        } catch (java.io.IOException e) {
            auditLogger.logFileUpload(username, originalFilename, imageFile.getSize(), "ERROR: " + e.getMessage());
            return null;
        }
    }
}
