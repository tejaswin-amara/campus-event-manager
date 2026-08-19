package com.tejaswin.campus.service;

import com.tejaswin.campus.model.Event;
import com.tejaswin.campus.model.RecommendedEvent;
import com.tejaswin.campus.model.Registration;
import com.tejaswin.campus.repository.EventRepository;
import com.tejaswin.campus.repository.RegistrationRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class RecommendationServiceTest {

    @Mock
    private EventRepository eventRepository;

    @Mock
    private RegistrationRepository registrationRepository;

    private RecommendationService recommendationService;

    @BeforeEach
    void setUp() {
        recommendationService = new RecommendationService(eventRepository, registrationRepository);
    }

    @Test
    void recommendsUnregisteredEventsUsingCategoryAffinity() {
        Event priorTechnicalEvent = event(1L, "Past technical event", "Technical", LocalDateTime.now().minusDays(2));
        Event matchingTechnicalEvent = event(2L, "Technical workshop", "Technical", LocalDateTime.now().plusDays(1));
        Event unrelatedCulturalEvent = event(3L, "Cultural festival", "Cultural", LocalDateTime.now().plusDays(2));
        Registration priorInterest = registration(11L, priorTechnicalEvent, "INTERESTED");

        when(registrationRepository.findByUserIdWithEvent(7L)).thenReturn(List.of(priorInterest));
        when(eventRepository.findByDateTimeAfterOrderByDateTimeAsc(any(LocalDateTime.class)))
                .thenReturn(List.of(matchingTechnicalEvent, unrelatedCulturalEvent));

        List<RecommendedEvent> result = recommendationService.recommendForUser(7L, 3);

        assertEquals(1, result.size());
        assertEquals(2L, result.get(0).getEvent().getId());
        assertTrue(result.get(0).getReasons().get(0).contains("Technical"));
    }

    @Test
    void popularitySignalCanOrderAndLimitRecommendations() {
        Event priorSportsEvent = event(4L, "Past sports event", "Sports", LocalDateTime.now().minusDays(3));
        Event popularSportsEvent = event(5L, "Popular sports event", "Sports", LocalDateTime.now().plusDays(3));
        popularSportsEvent.setMaxCapacity(10);
        Event secondSportsEvent = event(6L, "Second sports event", "Sports", LocalDateTime.now().plusDays(1));
        secondSportsEvent.setMaxCapacity(100);
        Registration priorInterest = registration(12L, priorSportsEvent, "ATTENDED");

        when(registrationRepository.findByUserIdWithEvent(7L)).thenReturn(List.of(priorInterest));
        when(eventRepository.findByDateTimeAfterOrderByDateTimeAsc(any(LocalDateTime.class)))
                .thenReturn(List.of(secondSportsEvent, popularSportsEvent));
        when(registrationRepository.countByEventId(5L)).thenReturn(9L);
        when(registrationRepository.countByEventId(6L)).thenReturn(1L);

        List<RecommendedEvent> result = recommendationService.recommendForUser(7L, 1);

        assertEquals(1, result.size());
        assertEquals(5L, result.get(0).getEvent().getId());
        assertTrue(result.get(0).getReasons().stream().anyMatch(reason -> reason.contains("Popular")));
    }

    @Test
    void invalidUserOrLimitReturnsEmptyRecommendations() {
        assertTrue(recommendationService.recommendForUser(null, 3).isEmpty());
        assertTrue(recommendationService.recommendForUser(7L, 0).isEmpty());
    }

    private Event event(Long id, String title, String category, LocalDateTime dateTime) {
        Event event = new Event();
        event.setId(id);
        event.setTitle(title);
        event.setCategory(category);
        event.setDateTime(dateTime);
        event.setVenue("Campus venue");
        event.setDescription("Description");
        return event;
    }

    private Registration registration(Long id, Event event, String status) {
        Registration registration = new Registration();
        registration.setId(id);
        registration.setEvent(event);
        registration.setStatus(status);
        return registration;
    }
}
