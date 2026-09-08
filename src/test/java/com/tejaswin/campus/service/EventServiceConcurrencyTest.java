package com.tejaswin.campus.service;

import com.tejaswin.campus.model.Event;
import com.tejaswin.campus.model.Registration;
import com.tejaswin.campus.model.User;
import com.tejaswin.campus.repository.EventRepository;
import com.tejaswin.campus.repository.RegistrationRepository;
import com.tejaswin.campus.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

/**
 * CO4 Verification: High-Contention Concurrency & ACID Stress Tests.
 *
 * Verifies that concurrent registration requests for the same (user_id, event_id)
 * pair are strictly serialized and protected by both row-level locking
 * (findByIdForUpdate) and the underlying relational UNIQUE constraint (uk_user_event).
 */
@SpringBootTest
public class EventServiceConcurrencyTest {

    @Autowired
    private EventService eventService;

    @Autowired
    private EventRepository eventRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RegistrationRepository registrationRepository;

    private Event testEvent;
    private User testUser;

    @BeforeEach
    void setUp() {
        registrationRepository.deleteAll();
        eventRepository.deleteAll();
        userRepository.deleteAll();

        testEvent = new Event();
        testEvent.setTitle("Concurrency Contention Workshop");
        testEvent.setDescription("High load stress test event");
        testEvent.setDateTime(LocalDateTime.now().plusDays(2));
        testEvent.setEndDateTime(LocalDateTime.now().plusDays(2).plusHours(3));
        testEvent.setVenue("CS Lab 404");
        testEvent.setCategory("Technical");
        testEvent.setStatus("PUBLISHED");
        testEvent.setMaxCapacity(100);
        testEvent = eventRepository.save(testEvent);

        testUser = new User();
        testUser.setUsername("stress_student_" + System.currentTimeMillis());
        testUser.setPassword("$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012");
        testUser.setRole("STUDENT");
        testUser.setEmail("stress_" + System.currentTimeMillis() + "@campus.edu");
        testUser = userRepository.save(testUser);
    }

    @Test
    @DisplayName("CO4: Concurrent registration attempts by the SAME user must yield exactly 1 success and N-1 safe rejections")
    void testConcurrentSameUserRegistrations() throws InterruptedException {
        int threadCount = 10;
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CountDownLatch readyLatch = new CountDownLatch(threadCount);
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch doneLatch = new CountDownLatch(threadCount);

        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger rejectedCount = new AtomicInteger(0);
        AtomicInteger errorCount = new AtomicInteger(0);

        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                readyLatch.countDown();
                try {
                    startLatch.await(); // Synchronous trigger for race condition
                    boolean registered = eventService.registerStudent(testEvent.getId(), testUser.getId());
                    if (registered) {
                        successCount.incrementAndGet();
                    } else {
                        rejectedCount.incrementAndGet();
                    }
                } catch (Exception e) {
                    errorCount.incrementAndGet();
                } finally {
                    doneLatch.countDown();
                }
            });
        }

        assertTrue(readyLatch.await(5, TimeUnit.SECONDS), "Threads failed to prepare");
        startLatch.countDown(); // Release all threads simultaneously
        assertTrue(doneLatch.await(10, TimeUnit.SECONDS), "Stress test execution timed out");
        executor.shutdown();

        // Invariant 1: Exactly 1 thread succeeds in creating the interest record
        assertEquals(1, successCount.get(), "Expected exactly 1 registration to succeed under race condition");
        // Invariant 2: N-1 threads are cleanly rejected without unhandled crash
        assertEquals(threadCount - 1, rejectedCount.get() + errorCount.get(), "All other concurrent attempts must be rejected");
        // Invariant 3: Relational state contains exactly 1 row for (user_id, event_id)
        List<Registration> registrations = registrationRepository.findByUserIdWithEvent(testUser.getId());
        assertEquals(1, registrations.size(), "Relational database must contain exactly one registration row");
    }

    @Test
    @DisplayName("CO4: Concurrent registration attempts by MULTIPLE distinct users must all succeed without deadlocks")
    void testConcurrentDistinctUsersRegistrations() throws InterruptedException {
        int userCount = 8;
        List<User> users = new ArrayList<>();
        for (int i = 0; i < userCount; i++) {
            User u = new User();
            u.setUsername("multi_user_" + i + "_" + System.currentTimeMillis());
            u.setPassword("$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012");
            u.setRole("STUDENT");
            u.setEmail("multi_" + i + "_" + System.currentTimeMillis() + "@campus.edu");
            users.add(userRepository.save(u));
        }

        ExecutorService executor = Executors.newFixedThreadPool(userCount);
        CountDownLatch readyLatch = new CountDownLatch(userCount);
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch doneLatch = new CountDownLatch(userCount);

        AtomicInteger successCount = new AtomicInteger(0);

        for (User u : users) {
            executor.submit(() -> {
                readyLatch.countDown();
                try {
                    startLatch.await();
                    boolean registered = eventService.registerStudent(testEvent.getId(), u.getId());
                    if (registered) {
                        successCount.incrementAndGet();
                    }
                } catch (Exception ignored) {
                } finally {
                    doneLatch.countDown();
                }
            });
        }

        readyLatch.await(5, TimeUnit.SECONDS);
        startLatch.countDown();
        doneLatch.await(10, TimeUnit.SECONDS);
        executor.shutdown();

        assertEquals(userCount, successCount.get(), "All distinct concurrent users must successfully register");
        assertEquals(userCount, registrationRepository.countByEventId(testEvent.getId()), "Event registration count must match distinct user count");
    }
}
