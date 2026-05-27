package com.rental.service;

import com.rental.dto.*;
import com.rental.model.User;
import com.rental.repository.UserRepository;
import com.rental.security.JwtUtil;
import com.rental.exception.RentalException;
import com.rental.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private static final Logger logger = LoggerFactory.getLogger(AuthService.class);

    private final UserRepository     userRepository;
    private final BCryptPasswordEncoder passwordEncoder;
    private final JwtUtil            jwtUtil;


    public AuthResponse register(RegisterRequest req) {
        logger.info("Starting registration for user: {}", req.getEmail());
        if (userRepository.existsByEmail(req.getEmail())) {
            logger.error("Registration failed: Email {} already exists", req.getEmail());
            throw new RentalException("Email already in use");
        }

        User user = new User();
        user.setUsername(req.getUsername());
        user.setEmail(req.getEmail());
        user.setPassword(passwordEncoder.encode(req.getPassword()));

        if (req.getRole() != null && req.getRole().equalsIgnoreCase("VEHICLE_OWNER")) {
            user.setRole(User.Role.VEHICLE_OWNER);
        } else {
            user.setRole(User.Role.USER);
        }

        userRepository.save(user); // saves to PostgreSQL
        logger.info("User {} registered successfully with role {}", user.getEmail(), user.getRole());

        String token = jwtUtil.generateToken(
                user.getEmail(), user.getRole().name());
        return new AuthResponse(
                token, user.getRole().name(), user.getUsername());
    }


    public AuthResponse login(LoginRequest req) {
        logger.info("Attempting login for user: {}", req.getEmail());
        User user = userRepository.findByEmail(req.getEmail())
                .orElseThrow(() -> {
                    logger.error("Login failed: User {} not found", req.getEmail());
                    return new ResourceNotFoundException("User not found with email: " + req.getEmail());
                });

        if (!passwordEncoder.matches(req.getPassword(), user.getPassword())) {
            logger.error("Login failed: Invalid password for user {}", req.getEmail());
            throw new RentalException("Invalid password");
        }

        logger.info("User {} logged in successfully", req.getEmail());
        String token = jwtUtil.generateToken(
                user.getEmail(), user.getRole().name());
        return new AuthResponse(
                token, user.getRole().name(), user.getUsername());
    }


    public User getCurrentUser() {
        String email = SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getName();

        return userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("Logged in user session not found"));
    }
}
