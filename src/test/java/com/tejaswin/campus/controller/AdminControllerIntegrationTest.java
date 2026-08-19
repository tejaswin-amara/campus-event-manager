package com.tejaswin.campus.controller;

import com.tejaswin.campus.service.SessionService;
import com.tejaswin.campus.model.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class AdminControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private SessionService sessionService;

    @BeforeEach
    void setUp() {
        User admin = new User();
        admin.setUsername("admin");
        admin.setRole("ADMIN");
        when(sessionService.getLoggedInUser()).thenReturn(admin);
        when(sessionService.isAdmin()).thenReturn(false);
    }

    @Test
    void whenAccessAdminDashboardWithoutSession_thenRedirectToLogin() throws Exception {
        mockMvc.perform(get("/admin/dashboard"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/login"));
    }

    @Test
    void whenPostWithoutCsrfToken_thenForbidden() throws Exception {
        mockMvc.perform(post("/admin/delete-event/1"))
                .andExpect(status().isForbidden());
    }

    @Test
    void whenPostWithCsrfTokenButNoSession_thenRedirectToLogin() throws Exception {
        mockMvc.perform(post("/admin/delete-event/1").with(csrf()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/login"));
    }

    @Test
    void adminDashboard_WithAdminUser_ShouldReturnOk() throws Exception {
        when(sessionService.isAdmin()).thenReturn(true);
        mockMvc.perform(get("/admin/dashboard").with(user("admin").roles("ADMIN")))
                .andExpect(status().isOk());
    }

    @Test
    void exportEventsCsv_WithAdminUser_ShouldReturnCsv() throws Exception {
        when(sessionService.isAdmin()).thenReturn(true);
        mockMvc.perform(get("/admin/export-events").with(user("admin").roles("ADMIN")))
                .andExpect(status().isOk())
                .andExpect(header().string("Content-Disposition", org.hamcrest.Matchers.containsString("attachment")))
                .andExpect(content().contentType("text/csv"));
    }
}
