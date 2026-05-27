package com.rental.controller;

import com.rental.dto.AuthResponse;
import com.rental.dto.LoginRequest;
import com.rental.dto.RegisterRequest;
import com.rental.service.AuthService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class AuthControllerTest {


    @Mock
    private AuthService authService;


    @InjectMocks
    private AuthController authController;

    @BeforeEach
    void setUp() {

        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testRegister_Success() {

        RegisterRequest request = new RegisterRequest();
        request.setUsername("New User");
        request.setEmail("new@example.com");

        AuthResponse fakeResponse = new AuthResponse("token123", "USER", "New User");
        

        when(authService.register(any(RegisterRequest.class))).thenReturn(fakeResponse);



        ResponseEntity<AuthResponse> response = authController.register(request);

        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());
        assertEquals("token123", response.getBody().getToken());
        assertEquals("New User", response.getBody().getUsername());
        

        verify(authService, times(1)).register(request);
    }

    @Test
    void testLogin_Success() {

        LoginRequest request = new LoginRequest();
        request.setEmail("user@example.com");
        request.setPassword("pass");

        AuthResponse fakeResponse = new AuthResponse("login-token", "USER", "user@example.com");
        when(authService.login(any(LoginRequest.class))).thenReturn(fakeResponse);


        ResponseEntity<AuthResponse> response = authController.login(request);


        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());
        assertEquals("login-token", response.getBody().getToken());
        
        verify(authService, times(1)).login(request);
    }
}
