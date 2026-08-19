package com.tejaswin.campus.model;

import java.util.List;

/**
 * A derived recommendation for the current student. It intentionally contains
 * no persisted state; MySQL remains authoritative for events and interests.
 */
public final class RecommendedEvent {
    private final Event event;
    private final int score;
    private final List<String> reasons;

    public RecommendedEvent(Event event, int score, List<String> reasons) {
        this.event = event;
        this.score = score;
        this.reasons = List.copyOf(reasons);
    }

    public Event getEvent() {
        return event;
    }

    public int getScore() {
        return score;
    }

    public List<String> getReasons() {
        return reasons;
    }
}
