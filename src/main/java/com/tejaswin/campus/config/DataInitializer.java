package com.tejaswin.campus.config;

import com.tejaswin.campus.model.Event;
import com.tejaswin.campus.model.User;
import com.tejaswin.campus.repository.EventRepository;
import com.tejaswin.campus.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.env.Environment;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import org.springframework.transaction.annotation.Transactional;

import java.security.SecureRandom;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Base64;

@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(DataInitializer.class);
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    private final UserRepository userRepository;
    private final EventRepository eventRepository;
    private final PasswordEncoder passwordEncoder;
    private final String configuredAdminPassword;

    @Autowired
    private Environment environment;

    public DataInitializer(UserRepository userRepository, EventRepository eventRepository,
            PasswordEncoder passwordEncoder,
            @Value("${app.admin-password:}") String adminPassword) {
        this.userRepository = userRepository;
        this.eventRepository = eventRepository;
        this.passwordEncoder = passwordEncoder;
        this.configuredAdminPassword = adminPassword == null ? "" : adminPassword.trim();
    }

    @Override
    @Transactional
    public void run(String... args) throws Exception {
        boolean production = Arrays.asList(environment.getActiveProfiles()).contains("prod");
        if (production && configuredAdminPassword.isBlank()) {
            throw new IllegalStateException(
                    "SECURITY: ADMIN_PASSWORD must be set when the prod profile is active.");
        }
        if (configuredAdminPassword.isBlank()) {
            logger.warn("ADMIN_PASSWORD is not set. A new admin account will receive an undisclosed bootstrap hash; set ADMIN_PASSWORD before production use.");
        }

        // 1. Ensure Guest User Exists (required for the public browsing experience)
        User guest = userRepository.findByUsernameForUpdate("guest").orElse(null);
        if (guest == null) {
            guest = new User();
            guest.setUsername("guest");
            guest.setPassword(passwordEncoder.encode("guest"));
            guest.setRole("STUDENT");
            userRepository.save(guest);
            logger.info("Guest user created for public browsing");
        } else if (guest.getPassword() != null && !isBCryptHash(guest.getPassword())) {
            guest.setPassword(passwordEncoder.encode(guest.getPassword()));
            userRepository.save(guest);
            logger.info("Guest password migrated to BCrypt");
        }

        // 2. Ensure Admin User Exists without shipping a known default password
        User admin = userRepository.findByUsernameForUpdate("admin").orElse(null);
        if (admin == null) {
            admin = new User();
            admin.setUsername("admin");
            String bootstrapPassword = configuredAdminPassword.isBlank()
                    ? generateUndisclosedBootstrapPassword()
                    : configuredAdminPassword;
            admin.setPassword(passwordEncoder.encode(bootstrapPassword));
            admin.setRole("ADMIN");
            userRepository.save(admin);
            logger.info("Admin user created; configure ADMIN_PASSWORD before attempting administrative login");
        } else if (admin.getPassword() != null && !isBCryptHash(admin.getPassword())) {
            admin.setPassword(passwordEncoder.encode(admin.getPassword()));
            userRepository.save(admin);
            logger.info("Admin password migrated to BCrypt");
        } else if (!configuredAdminPassword.isBlank()
                && admin.getPassword() != null
                && !passwordEncoder.matches(configuredAdminPassword, admin.getPassword())) {
            admin.setPassword(passwordEncoder.encode(configuredAdminPassword));
            userRepository.save(admin);
            logger.info("Admin password updated to match configured ADMIN_PASSWORD");
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
            logger.info("Sample welcome event created");
        }
    }

    private String generateUndisclosedBootstrapPassword() {
        byte[] randomBytes = new byte[32];
        SECURE_RANDOM.nextBytes(randomBytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(randomBytes);
    }

    /**
     * Returns true if the given password string is already a BCrypt hash.
     * BCrypt hashes always start with "$2a$", "$2b$", or "$2y$".
     */
    private boolean isBCryptHash(String password) {
        return password.startsWith("$2a$") || password.startsWith("$2b$") || password.startsWith("$2y$");
    }
}
