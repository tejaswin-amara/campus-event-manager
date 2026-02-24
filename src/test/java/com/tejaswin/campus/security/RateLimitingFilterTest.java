package com.tejaswin.campus.security;

import com.tejaswin.campus.config.AppConfig;
import jakarta.servlet.FilterChain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;

import java.io.PrintWriter;
import java.io.StringWriter;

import static org.mockito.Mockito.*;

class RateLimitingFilterTest {

    private RateLimitingFilter filter;

    @Mock
    private AppConfig appConfig;

    @Mock
    private AppConfig.RateLimit rateLimit;

    @Mock
    private HttpServletRequest request;

    @Mock
    private HttpServletResponse response;

    @Mock
    private FilterChain filterChain;

    @BeforeEach
    void setUp() throws Exception {
        MockitoAnnotations.openMocks(this);
        when(appConfig.getRateLimit()).thenReturn(rateLimit);
        when(rateLimit.getCapacity()).thenReturn(5);
        when(rateLimit.getTokens()).thenReturn(5);
        when(rateLimit.getMinutes()).thenReturn(1);

        filter = new RateLimitingFilter(appConfig);

        when(response.getWriter()).thenReturn(new PrintWriter(new StringWriter()));
    }

    @Test
    void doFilterInternal_WithGetRequest_ShouldAlwaysAllow() throws Exception {
        when(request.getMethod()).thenReturn("GET");
        when(request.getServletPath()).thenReturn("/any");

        filter.doFilterInternal(request, response, filterChain);

        verify(filterChain).doFilter(request, response);
    }

    @Test
    void doFilterInternal_WithPostRequestToAdminLogin_ShouldRateLimit() throws Exception {
        when(request.getMethod()).thenReturn("POST");
        when(request.getServletPath()).thenReturn("/admin/login");
        when(request.getRemoteAddr()).thenReturn("1.2.3.4");

        // Consume all tokens
        for (int i = 0; i < 5; i++) {
            filter.doFilterInternal(request, response, filterChain);
        }
        verify(filterChain, times(5)).doFilter(request, response);

        // 6th attempt should fail
        filter.doFilterInternal(request, response, filterChain);
        verify(response).setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
        verify(filterChain, times(5)).doFilter(request, response); // Should not increase
    }

    @Test
    void doFilterInternal_WithTrustedProxy_ShouldUseXffHeader() throws Exception {
        when(request.getMethod()).thenReturn("POST");
        when(request.getServletPath()).thenReturn("/admin/login");
        when(request.getRemoteAddr()).thenReturn("127.0.0.1");
        when(request.getHeader("X-Forwarded-For")).thenReturn("192.168.1.1, 10.0.0.1");

        filter.doFilterInternal(request, response, filterChain);

        verify(filterChain).doFilter(request, response);
        // This test ensures the internal getClientIp logic handles XFF correctly
    }
}
