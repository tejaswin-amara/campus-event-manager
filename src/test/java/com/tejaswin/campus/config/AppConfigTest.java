package com.tejaswin.campus.config;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AppConfigTest {

    @Test
    void appConfig_ShouldHandleRateLimitProperties() {
        AppConfig config = new AppConfig();
        AppConfig.RateLimit rateLimit = new AppConfig.RateLimit();
        rateLimit.setCapacity(10);
        rateLimit.setTokens(10);
        rateLimit.setMinutes(5);
        config.setRateLimit(rateLimit);

        assertEquals(10, config.getRateLimit().getCapacity());
        assertEquals(10, config.getRateLimit().getTokens());
        assertEquals(5, config.getRateLimit().getMinutes());
    }

    @Test
    void appConfig_ShouldHandleUploadDir() {
        AppConfig config = new AppConfig();
        config.setUploadDir("test-uploads");
        assertEquals("test-uploads", config.getUploadDir());
    }
}
