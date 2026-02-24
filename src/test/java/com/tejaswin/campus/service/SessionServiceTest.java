package com.tejaswin.campus.service;

import com.tejaswin.campus.model.User;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class SessionServiceTest {

    private SessionService sessionService;

    @Mock
    private HttpSession session;

    @Mock
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        sessionService = new SessionService();

        ServletRequestAttributes attr = new ServletRequestAttributes(request);
        RequestContextHolder.setRequestAttributes(attr);

        when(request.getSession(anyBoolean())).thenReturn(session);
    }

    @Test
    void setLoggedInUser_ShouldStoreUserInSession() {
        User user = new User();
        user.setUsername("testUser");

        sessionService.setLoggedInUser(user);

        verify(session).setAttribute("loggedInUser", user);
    }

    @Test
    void getLoggedInUser_WithUserInSession_ShouldReturnUser() {
        User user = new User();
        when(session.getAttribute("loggedInUser")).thenReturn(user);

        User result = sessionService.getLoggedInUser();

        assertEquals(user, result);
    }

    @Test
    void invalidateSession_ShouldInvalidate() {
        sessionService.invalidateSession();
        verify(session).invalidate();
    }

    @Test
    void isAdmin_WithAdminUser_ShouldReturnTrue() {
        User user = new User();
        user.setRole("ADMIN");
        when(session.getAttribute("loggedInUser")).thenReturn(user);

        assertTrue(sessionService.isAdmin());
    }
}
