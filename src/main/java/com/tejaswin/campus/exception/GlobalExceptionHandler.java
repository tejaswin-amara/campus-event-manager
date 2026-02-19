package com.tejaswin.campus.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.servlet.NoHandlerFoundException;

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

    @ExceptionHandler(Exception.class)
    public String handleGenericException(Exception exc, Model model) {
        logger.error("Unhandled exception caught by GlobalExceptionHandler", exc);
        model.addAttribute("message", "An unexpected error occurred. Please try again later.");
        model.addAttribute("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        return "error";
    }
}
