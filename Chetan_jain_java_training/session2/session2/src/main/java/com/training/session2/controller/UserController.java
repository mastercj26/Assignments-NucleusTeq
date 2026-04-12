package com.training.session2.controller;

import com.training.session2.model.User;
import com.training.session2.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public ResponseEntity<Map<String, Object>> getAllUsers() {

        List<User> users = userService.getAllUsers();

        Map<String, Object> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("count", users.size());
        response.put("users", users);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Map<String, Object>> getUserById(@PathVariable int id) {

        User user = userService.getUserById(id);

        Map<String, Object> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("user", user);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> createUser(@RequestBody User user) {

        User createdUser = userService.createUser(user);

        Map<String, Object> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("message", "User created successfully");
        response.put("user", createdUser);

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }
}