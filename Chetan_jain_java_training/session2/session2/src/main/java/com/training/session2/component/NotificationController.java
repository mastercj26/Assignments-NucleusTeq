package com.training.session2.controller;

import com.training.session2.service.NotificationService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/notifications")
public class NotificationController {

    private final NotificationService notificationService;

    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    @PostMapping("/trigger")
    public ResponseEntity<Map<String, Object>> triggerNotification(@RequestBody Map<String, String> request) {

        String recipient = request.get("recipient");
        String action = request.get("action");

        if (recipient == null || action == null) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("status", "ERROR");
            errorResponse.put("message", "recipient and action fields are required");
            return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
        }

        List<String> notifications = notificationService.triggerNotifications(recipient, action);

        Map<String, Object> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("message", "Notification sent");
        response.put("notificationsSent", notifications);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @GetMapping("/trigger")
    public ResponseEntity<Map<String, Object>> triggerSingleNotification(
            @RequestParam String type,
            @RequestParam String recipient,
            @RequestParam String action) {

        String result = notificationService.triggerSingleNotification(type, recipient, action);

        Map<String, Object> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("message", "Notification sent");
        response.put("notification", result);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}