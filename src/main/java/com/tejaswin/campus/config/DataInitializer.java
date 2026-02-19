package com.tejaswin.campus.config;

import com.tejaswin.campus.model.Event;
import com.tejaswin.campus.model.User;
import com.tejaswin.campus.repository.EventRepository;
import com.tejaswin.campus.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(DataInitializer.class);
    private final UserRepository userRepository;
    private final EventRepository eventRepository;
    private final String adminPassword;

    public DataInitializer(UserRepository userRepository, EventRepository eventRepository,
            @Value("${app.admin-password:admin123}") String adminPassword) {
        this.userRepository = userRepository;
        this.eventRepository = eventRepository;
        this.adminPassword = adminPassword;
    }

    @Override
    public void run(String... args) throws Exception {
        // 1. Ensure Guest User Exists (CRITICAL: Required for auto-login on /)
        if (userRepository.findByUsername("guest").isEmpty()) {
            User guest = new User();
            guest.setUsername("guest");
            guest.setPassword("guest");
            guest.setRole("STUDENT");
            userRepository.save(guest);
            logger.info("✅ Guest user created (auto-login enabled)");
        }

        // 2. Ensure Admin User Exists
        if (userRepository.findByUsername("admin").isEmpty()) {
            User admin = new User();
            admin.setUsername("admin");
            admin.setPassword(adminPassword);
            admin.setRole("ADMIN");
            userRepository.save(admin);
            logger.info("✅ Admin user created");
        }

        // 3. Ensure Sample Event Exists
        if (eventRepository.count() == 0) {
            Event welcomeEvent = new Event();
            welcomeEvent.setTitle("Welcome to CampusConnect!");
            welcomeEvent.setDescription(
                    "This is a sample event to show you around. You can register for events, view details, and more! Admins can delete this event from the admin dashboard.");
            welcomeEvent.setVenue("Virtual Campus");
            welcomeEvent.setCategory("Technical");
            welcomeEvent.setDateTime(LocalDateTime.now().plusDays(7));
            welcomeEvent.setEndDateTime(LocalDateTime.now().plusDays(7).plusHours(2));
            welcomeEvent.setMaxCapacity(100);

            eventRepository.save(welcomeEvent);
            logger.info("✅ Sample 'Welcome' event created.");
        }
    }
}
