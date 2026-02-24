package com.tejaswin.campus.security;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

@SpringBootTest
class SecurityAuditLoggerTest {

    @Autowired
    private SecurityAuditLogger auditLogger;

    @Test
    void logLoginAttempt_ShouldNotThrow() {
        assertDoesNotThrow(() -> auditLogger.logLoginAttempt("admin", true, "127.0.0.1", "Mozilla/5.0"));
    }

    @Test
    void logSecurityLinkClick_ShouldNotThrow() {
        assertDoesNotThrow(() -> auditLogger.logSecurityLinkClick("admin", "TEST", 1L));
    }

    @Test
    void logFileUpload_ShouldNotThrow() {
        assertDoesNotThrow(() -> auditLogger.logFileUpload("admin", "test.txt", 1024L, "SUCCESS"));
    }
}
