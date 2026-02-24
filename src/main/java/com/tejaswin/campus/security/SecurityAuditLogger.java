package com.tejaswin.campus.security;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;

@Component
public class SecurityAuditLogger {
    private static final Logger logger = LoggerFactory.getLogger(SecurityAuditLogger.class);

    public void logLoginAttempt(String username, boolean success, String ip, String userAgent) {
        try {
            MDC.put("event_type", "LOGIN_ATTEMPT");
            MDC.put("login_user", username);
            MDC.put("login_success", String.valueOf(success));
            MDC.put("client_ip", ip);
            MDC.put("user_agent", userAgent);

            if (success) {
                logger.info("AUDIT: Successful login for user: {}", username);
            } else {
                logger.warn("AUDIT: Failed login attempt for user: {} from IP: {}", username, ip);
            }
        } finally {
            MDC.clear();
        }
    }

    public void logFileUpload(String username, String fileName, long size, String result) {
        try {
            MDC.put("event_type", "FILE_UPLOAD");
            MDC.put("upload_user", username);
            MDC.put("file_name", fileName);
            MDC.put("file_size", String.valueOf(size));
            MDC.put("upload_result", result);

            logger.info("AUDIT: File upload attempt: {} by user: {} - Status: {}", fileName, username, result);
        } finally {
            MDC.clear();
        }
    }

    public void logSecurityLinkClick(String username, String linkType, Long targetId) {
        try {
            MDC.put("event_type", "SECURITY_LINK_CLICK");
            MDC.put("user", username);
            MDC.put("link_type", linkType);
            MDC.put("target_id", String.valueOf(targetId));

            logger.info("AUDIT: User {} clicked security link {} for target ID {}", username, linkType, targetId);
        } finally {
            MDC.clear();
        }
    }
}
