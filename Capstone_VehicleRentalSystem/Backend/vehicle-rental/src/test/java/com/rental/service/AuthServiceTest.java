package com.rental.service;

import com.rental.dto.AuthResponse;
import com.rental.dto.LoginRequest;
import com.rental.model.User;
import com.rental.repository.UserRepository;
import com.rental.security.JwtUtil;
import com.rental.exception.ResourceNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class AuthServiceTest {


    @Mock
    private UserRepository userRepository;

    @Mock
    private BCryptPasswordEncoder passwordEncoder;

    @Mock
    private JwtUtil jwtUtil;


    @InjectMocks
    private AuthService authService;

    @BeforeEach
    void setUp() {

        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testLogin_Success() {

        LoginRequest loginRequest = new LoginRequest();
        loginRequest.setEmail("test@example.com");
        loginRequest.setPassword("password123");

        User fakeUser = new User();
        fakeUser.setEmail("test@example.com");
        fakeUser.setPassword("encodedPassword");
        fakeUser.setRole(User.Role.USER);
        fakeUser.setUsername("Test User");


        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(fakeUser));
        when(passwordEncoder.matches("password123", "encodedPassword")).thenReturn(true);
        when(jwtUtil.generateToken(anyString(), anyString())).thenReturn("fake-jwt-token");


        AuthResponse response = authService.login(loginRequest);

        assertNotNull(response);
        assertEquals("fake-jwt-token", response.getToken());
        assertEquals("USER", response.getRole());
        assertEquals("Test User", response.getUsername());

        verify(userRepository, times(1)).findByEmail("test@example.com");
        verify(passwordEncoder, times(1)).matches("password123", "encodedPassword");
    }

    @Test
    void testLogin_UserNotFound() {

        LoginRequest loginRequest = new LoginRequest();
        loginRequest.setEmail("notfound@example.com");

        when(userRepository.findByEmail("notfound@example.com")).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> {
            authService.login(loginRequest);
        });
    }
}
