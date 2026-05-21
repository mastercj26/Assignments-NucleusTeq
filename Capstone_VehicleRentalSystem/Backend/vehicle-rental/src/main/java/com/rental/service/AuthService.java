package com.rental.service;

import com.rental.dto.AuthResponse;
import com.rental.dto.LoginRequest;
import com.rental.dto.RegisterRequest;
import com.rental.model.User;
import com.rental.repository.UserRepository;
import com.rental.security.JwtUtil;

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private UserRepository userRepository;

    private BCryptPasswordEncoder passwordEncoder;

    private JwtUtil jwtUtil;

    public AuthService(UserRepository userRepository,
                       BCryptPasswordEncoder passwordEncoder,
                       JwtUtil jwtUtil) {

        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
    }

    public AuthResponse register(RegisterRequest req) {

        Boolean emailExists =
                userRepository.existsByEmail(req.getEmail());

        if (emailExists) {
            throw new RuntimeException("Email already exists");
        }

        User user = new User();

        user.setUsername(req.getUsername());

        user.setEmail(req.getEmail());

        user.setPassword(
                passwordEncoder.encode(req.getPassword())
        );

        if (req.getRole() != null &&
                req.getRole().equalsIgnoreCase("VEHICLE_OWNER")) {

            user.setRole(User.Role.VEHICLE_OWNER);

        } else {

            user.setRole(User.Role.USER);
        }

        userRepository.save(user);

        String token = jwtUtil.generateToken(
                user.getEmail(),
                user.getRole().name()
        );

        return new AuthResponse(
                token,
                user.getRole().name(),
                user.getUsername()
        );
    }

    public AuthResponse login(LoginRequest req) {

        User user = userRepository.findByEmail(req.getEmail())
                .orElseThrow(() ->
                        new RuntimeException("User not found")
                );

        boolean passwordMatch =
                passwordEncoder.matches(
                        req.getPassword(),
                        user.getPassword()
                );

        if (!passwordMatch) {
            throw new RuntimeException("Wrong password");
        }

        String token = jwtUtil.generateToken(
                user.getEmail(),
                user.getRole().name()
        );

        return new AuthResponse(
                token,
                user.getRole().name(),
                user.getUsername()
        );
    }

    public User getCurrentUser() {

        String email = SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getName();

        return userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new RuntimeException("User not found")
                );
    }
}