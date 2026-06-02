package com.training.userapi.controller;

import com.training.userapi.model.User;
import com.training.userapi.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/users/search")
    public ResponseEntity<Object> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role) {

        List<User> result = userService.searchUsers(name, age, role);

        Map<String, Object> response = new HashMap<>();

        if (result.isEmpty()) {
            response.put("message", "No users found matching the given criteria");
            response.put("data", result);
            response.put("count", 0);
            return ResponseEntity.ok(response);
        }

        response.put("message", "Users fetched successfully");
        response.put("data", result);
        response.put("count", result.size());

        return ResponseEntity.ok(response);
    }

    @PostMapping("/submit")
    public ResponseEntity<Object> submitUser(@RequestBody User user) {

        String result = userService.addUser(user);

        Map<String, Object> response = new HashMap<>();

        if (result.equals("SUCCESS")) {
            response.put("message", "User added successfully");
            response.put("status", "success");

            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } else {
            response.put("message", result);
            response.put("status", "error");

            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
        }
    }

    @DeleteMapping("/users/{id}")
    public ResponseEntity<Object> deleteUser(
            @PathVariable int id,
            @RequestParam(defaultValue = "false") boolean confirm) {

        String result = userService.deleteUser(id, confirm);

        Map<String, Object> response = new HashMap<>();

        if (result.equals("CONFIRMATION_REQUIRED")) {

            response.put("message", "Confirmation required. Please add ?confirm=true to delete.");
            response.put("status", "warning");

            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);

        } else if (result.equals("NOT_FOUND")) {

            response.put("message", "User with ID " + id + " not found");
            response.put("status", "error");

            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);

        } else {

            response.put("message", "User with ID " + id + " deleted successfully");
            response.put("status", "success");

            return ResponseEntity.ok(response);
        }
    }
}