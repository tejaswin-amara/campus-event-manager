package com.tejaswin.campus.model;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

class EventTest {

    @Test
    void constructorAndAccessorsPreserveEventData() {
        LocalDateTime start = LocalDateTime.of(2026, 9, 1, 10, 0);
        LocalDateTime end = start.plusHours(2);
        Event event = new Event(7L, "Orientation", "Welcome", start, "Hall A", "Workshop");
        byte[] image = {1, 2, 3};

        event.setId(8L);
        event.setTitle("Updated Orientation");
        event.setDescription("Updated description");
        event.setDateTime(start.plusDays(1));
        event.setEndDateTime(end);
        event.setVenue("Hall B");
        event.setCategory("Seminar");
        event.setRegistrationLink("https://example.com/register");
        event.setMaxCapacity(100);
        event.setImageUrl("/uploads/event.png");
        event.setResponsesLink("https://example.com/responses");
        event.setImageData(image);
        event.setImageMimeType("image/png");

        assertEquals(8L, event.getId());
        assertEquals("Updated Orientation", event.getTitle());
        assertEquals("Updated description", event.getDescription());
        assertEquals(start.plusDays(1), event.getDateTime());
        assertEquals(end, event.getEndDateTime());
        assertEquals("Hall B", event.getVenue());
        assertEquals("Seminar", event.getCategory());
        assertEquals("https://example.com/register", event.getRegistrationLink());
        assertEquals(100, event.getMaxCapacity());
        assertEquals("/uploads/event.png", event.getImageUrl());
        assertEquals("https://example.com/responses", event.getResponsesLink());
        assertArrayEquals(image, event.getImageData());
        assertEquals("image/png", event.getImageMimeType());
        assertEquals("Event{id=8, title='Updated Orientation', category='Seminar', dateTime=" + start.plusDays(1) + "}", event.toString());
    }
}
