package com.tejaswin.campus.exception;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.stereotype.Controller;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.bind.annotation.GetMapping;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Import(GlobalExceptionHandlerTest.ExceptionTriggerController.class)
class GlobalExceptionHandlerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void handleEventNotFoundException_ShouldReturn404View() throws Exception {
        mockMvc.perform(get("/test/trigger-404"))
                .andExpect(status().isNotFound())
                .andExpect(view().name("error"));
    }

    @Test
    void handleGenericException_ShouldReturnErrorView() throws Exception {
        mockMvc.perform(get("/test/trigger-500"))
                .andExpect(status().isInternalServerError())
                .andExpect(view().name("error"));
    }

    @Controller
    public static class ExceptionTriggerController {
        @GetMapping("/test/trigger-404")
        public void trigger404() {
            throw new EventNotFoundException("Not found");
        }

        @GetMapping("/test/trigger-500")
        public void trigger500() {
            throw new RuntimeException("Generic error");
        }
    }
}
