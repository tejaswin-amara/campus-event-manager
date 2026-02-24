package com.tejaswin.campus.controller;

import com.tejaswin.campus.model.User;
import com.tejaswin.campus.service.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    private User adminUser;

    @BeforeEach
    void setUp() {
        adminUser = new User();
        adminUser.setId(1L);
        adminUser.setUsername("admin");
        adminUser.setPassword("hashedPassword");
        adminUser.setRole("ADMIN");
    }

    @Test
    void showAdminLogin_ShouldReturnLoginView() throws Exception {
        mockMvc.perform(get("/admin/login"))
                .andExpect(status().isOk())
                .andExpect(view().name("admin_login"));
    }

    @Test
    void adminLogin_WithValidCredentials_ShouldRedirectToDashboard() throws Exception {
        when(userService.authenticate("admin", "admin123")).thenReturn(adminUser);

        mockMvc.perform(post("/admin/login")
                .param("username", "admin")
                .param("password", "admin123")
                .with(csrf()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/dashboard"));
    }

    @Test
    void adminLogin_WithInvalidCredentials_ShouldRedirectWithError() throws Exception {
        when(userService.authenticate(anyString(), anyString())).thenReturn(null);

        mockMvc.perform(post("/admin/login")
                .param("username", "invalid")
                .param("password", "wrong")
                .with(csrf()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/login"))
                .andExpect(flash().attributeExists("error"));
    }

    @Test
    void logout_ShouldInvalidateSessionAndRedirectToRoot() throws Exception {
        mockMvc.perform(post("/logout")
                .with(csrf()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/"));
    }
}
