package com.rental.service;

import com.rental.dto.*;
import com.rental.model.User;
import com.rental.repository.UserRepository;
import com.rental.security.JwtUtil;
import com.rental.exception.RentalException;
import com.rental.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository     userRepository;
    private final BCryptPasswordEncoder passwordEncoder;
    private final JwtUtil            jwtUtil;

    // ── REGISTER ──
    public AuthResponse register(RegisterRequest req) {
        if (userRepository.existsByEmail(req.getEmail()))
            throw new RentalException("Email already in use");

        User user = new User();
        user.setUsername(req.getUsername());
        user.setEmail(req.getEmail());
        user.setPassword(passwordEncoder.encode(req.getPassword()));
        
        // Allow choosing role, default to USER
        if (req.getRole() != null && req.getRole().equalsIgnoreCase("VEHICLE_OWNER")) {
            user.setRole(User.Role.VEHICLE_OWNER);
        } else {
            user.setRole(User.Role.USER);
        }

        userRepository.save(user); // saves to PostgreSQL

        String token = jwtUtil.generateToken(
                user.getEmail(), user.getRole().name());
        return new AuthResponse(
                token, user.getRole().name(), user.getUsername());
    }

    // ── LOGIN ──
    public AuthResponse login(LoginRequest req) {
        User user = userRepository.findByEmail(req.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User not found with email: " + req.getEmail()));

        if (!passwordEncoder.matches(req.getPassword(), user.getPassword()))
            throw new RentalException("Invalid password");

        String token = jwtUtil.generateToken(
                user.getEmail(), user.getRole().name());
        return new AuthResponse(
                token, user.getRole().name(), user.getUsername());
    }

    // ── GET CURRENTLY LOGGED IN USER ──
    // Used by BookingService to know who is making the booking
    public User getCurrentUser() {
        String email = SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getName(); // this is the email we stored in JWT subject

        return userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("Logged in user session not found"));
    }
}
