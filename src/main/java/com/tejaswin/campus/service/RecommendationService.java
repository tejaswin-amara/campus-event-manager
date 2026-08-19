package com.tejaswin.campus.service;

import com.tejaswin.campus.model.Event;
import com.tejaswin.campus.model.RecommendedEvent;
import com.tejaswin.campus.model.Registration;
import com.tejaswin.campus.repository.EventRepository;
import com.tejaswin.campus.repository.RegistrationRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Derives a small, explainable recommendation list from relational data.
 *
 * <p>The scoring is deliberately simple: category affinity is learned from
 * prior interest/attendance, and a high event fill rate contributes a modest
 * popularity signal. No client-supplied score, Firebase document, or vector
 * index is trusted for this decision.</p>
 */
@Service
public class RecommendationService {

    private final EventRepository eventRepository;
    private final RegistrationRepository registrationRepository;

    public RecommendationService(EventRepository eventRepository,
            RegistrationRepository registrationRepository) {
        this.eventRepository = eventRepository;
        this.registrationRepository = registrationRepository;
    }

    @Transactional(readOnly = true)
    public List<RecommendedEvent> recommendForUser(Long userId, int limit) {
        if (userId == null || limit <= 0) {
            return List.of();
        }

        List<Registration> registrations = registrationRepository.findByUserIdWithEvent(userId);
        Set<Long> registeredEventIds = new HashSet<>();
        Map<String, Integer> categoryWeights = new HashMap<>();

        for (Registration registration : registrations) {
            Event event = registration.getEvent();
            if (event == null || event.getId() == null) {
                continue;
            }
            registeredEventIds.add(event.getId());
            if (event.getCategory() != null && !event.getCategory().isBlank()) {
                int weight = "ATTENDED".equalsIgnoreCase(registration.getStatus()) ? 3 : 1;
                categoryWeights.merge(event.getCategory(), weight, Integer::sum);
            }
        }

        List<RecommendedEvent> recommendations = new ArrayList<>();
        for (Event event : eventRepository.findByDateTimeAfterOrderByDateTimeAsc(LocalDateTime.now())) {
            if (event.getId() == null || registeredEventIds.contains(event.getId())) {
                continue;
            }

            int score = 0;
            List<String> reasons = new ArrayList<>();
            int categoryWeight = categoryWeights.getOrDefault(event.getCategory(), 0);
            if (categoryWeight > 0) {
                score += categoryWeight * 6;
                reasons.add("Based on your interest in " + event.getCategory() + " events");
            }

            Integer capacity = event.getMaxCapacity();
            if (capacity != null && capacity > 0) {
                long registeredCount = event.getId() == null ? 0
                        : registrationRepository.countByEventId(event.getId());
                double fillRate = (double) registeredCount / capacity;
                if (fillRate > 0.8d) {
                    score += 8;
                    reasons.add("Popular choice: seats are filling up");
                }
            }

            if (score > 0) {
                recommendations.add(new RecommendedEvent(
                        event,
                        score,
                        reasons.isEmpty() ? List.of("Recommended for you") : reasons));
            }
        }

        return recommendations.stream()
                .sorted(Comparator.comparingInt(RecommendedEvent::getScore)
                        .reversed()
                        .thenComparing(recommendation -> recommendation.getEvent().getDateTime()))
                .limit(limit)
                .toList();
    }
}
