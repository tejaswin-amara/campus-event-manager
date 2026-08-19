package com.tejaswin.campus.model;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

class RecommendedEventTest {

    @Test
    void preservesEventScoreAndImmutableReasons() {
        Event event = new Event();
        List<String> reasons = List.of("category affinity", "popular");

        RecommendedEvent recommendation = new RecommendedEvent(event, 87, reasons);

        assertSame(event, recommendation.getEvent());
        assertEquals(87, recommendation.getScore());
        assertEquals(reasons, recommendation.getReasons());
    }
}
