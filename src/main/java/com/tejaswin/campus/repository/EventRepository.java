package com.tejaswin.campus.repository;

import com.tejaswin.campus.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface EventRepository extends JpaRepository<Event, Long> {

    List<Event> findAllByOrderByDateTimeDesc();

    long countByDateTimeAfter(LocalDateTime dateTime);

    List<Event> findByTitleContainingIgnoreCaseOrVenueContainingIgnoreCase(String title, String venue);

    List<Event> findByCategoryOrderByDateTimeDesc(String category);

    @Query("SELECT e.category, COUNT(e) FROM Event e GROUP BY e.category")
    List<Object[]> countEventsByCategory();
}
