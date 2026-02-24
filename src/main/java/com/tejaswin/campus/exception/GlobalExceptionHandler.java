package com.tejaswin.campus.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.servlet.NoHandlerFoundException;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@ControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public String handleMaxSizeException(MaxUploadSizeExceededException exc, Model model) {
        logger.warn("File upload size exceeded: {}", exc.getMessage());
        model.addAttribute("errorMessage", "File is too large! Please upload a smaller file.");
        model.addAttribute("status", HttpStatus.PAYLOAD_TOO_LARGE.value());
        return "error";
    }

    @ExceptionHandler(NoHandlerFoundException.class)
    public String handleNotFound(NoHandlerFoundException exc, Model model) {
        logger.debug("Page not found: {}", exc.getRequestURL());
        model.addAttribute("message", "The page you requested could not be found.");
        model.addAttribute("status", HttpStatus.NOT_FOUND.value());
        return "error";
    }

    @ExceptionHandler(EventNotFoundException.class)
    public String handleEventNotFound(EventNotFoundException exc,
            org.springframework.web.servlet.mvc.support.RedirectAttributes redirectAttributes) {
        logger.warn("Event not found: {}", exc.getMessage());
        redirectAttributes.addFlashAttribute("error", exc.getMessage());
        return "redirect:/admin/dashboard";
    }

    @ExceptionHandler(InvalidImageException.class)
    public String handleInvalidImage(InvalidImageException exc,
            org.springframework.web.servlet.mvc.support.RedirectAttributes redirectAttributes) {
        logger.warn("Invalid image upload: {}", exc.getMessage());
        redirectAttributes.addFlashAttribute("error", exc.getMessage());
        return "redirect:/admin/dashboard";
    }

    @ExceptionHandler(org.springframework.security.access.AccessDeniedException.class)
    public String handleAccessDenied(org.springframework.security.access.AccessDeniedException exc, Model model) {
        logger.warn("Security Access Denied: {}", exc.getMessage());
        model.addAttribute("message", "You do not have permission to access this resource.");
        model.addAttribute("status", HttpStatus.FORBIDDEN.value());
        return "error";
    }

    @ExceptionHandler(org.springframework.security.core.AuthenticationException.class)
    public String handleAuthenticationException(org.springframework.security.core.AuthenticationException exc,
            RedirectAttributes redirectAttributes) {
        logger.warn("Authentication failure: {}", exc.getMessage());
        redirectAttributes.addFlashAttribute("error",
                "Your session has expired or authentication failed. Please login again.");
        return "redirect:/admin/login";
    }

    @ExceptionHandler(Exception.class)
    public String handleGenericException(Exception exc, Model model) {
        logger.error("Unhandled exception caught by GlobalExceptionHandler", exc);
        model.addAttribute("message", "An unexpected error occurred. Please try again later.");
        model.addAttribute("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        return "error";
    }
}
