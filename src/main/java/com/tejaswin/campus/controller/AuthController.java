package com.tejaswin.campus.controller;

import com.tejaswin.campus.model.User;
import com.tejaswin.campus.service.UserService;
import jakarta.servlet.http.HttpSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
public class AuthController {

    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);

    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/")
    public String root(HttpSession session) {
        // Auto-login as Guest Student
        User guest = userService.getGuestUser();
        logger.debug("Root accessed. Guest user found? {}", (guest != null));
        if (guest != null) {
            session.setAttribute("loggedInUser", guest);
            logger.info("Guest logged in. Session ID: {}", session.getId());
            return "redirect:/student/dashboard";
        }
        logger.warn("Guest user NOT found. Redirecting to admin login.");
        return "redirect:/admin/login"; // Fallback if guest user missing
    }

    @GetMapping("/admin/login")
    public String adminLoginPage() {
        return "admin_login";
    }

    @PostMapping("/admin/login")
    public String adminLogin(@RequestParam String username,
            @RequestParam String password,
            HttpSession session,
            RedirectAttributes redirectAttributes) {

        User user = userService.authenticate(username, password);

        if (user == null || !"ADMIN".equals(user.getRole())) {
            redirectAttributes.addFlashAttribute("error", "Invalid admin credentials!");
            return "redirect:/admin/login";
        }

        session.setAttribute("loggedInUser", user);
        return "redirect:/admin/dashboard";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/";
    }
}
