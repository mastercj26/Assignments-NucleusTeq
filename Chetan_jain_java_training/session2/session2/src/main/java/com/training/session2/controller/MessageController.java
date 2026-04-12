package com.training.session2.controller;

import com.training.session2.service.MessageService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/message")
public class MessageController {

    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    @GetMapping
    public ResponseEntity<Map<String, Object>> getMessage(
            @RequestParam String type,
            @RequestParam(defaultValue = "General Update") String topic) {

        String formattedMessage = messageService.getFormattedMessage(type, topic);

        Map<String, Object> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("requestedType", type.toUpperCase());
        response.put("topic", topic);
        response.put("message", formattedMessage);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @GetMapping("/types")
    public ResponseEntity<Map<String, Object>> getAvailableTypes() {

        Map<String, Object> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("availableTypes", messageService.getAvailableFormatterTypes());
        response.put("usage", "Use GET /message?type=SHORT&topic=YourTopic");

        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}