package com.rental.exception;

import com.rental.dto.ErrorResponse;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class GlobalExceptionHandlerTest {

    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test
    void handleResourceNotFound() {
        ResourceNotFoundException ex = new ResourceNotFoundException("Not found");
        ResponseEntity<ErrorResponse> response = handler.handleResourceNotFound(ex);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals("Not found", response.getBody().getMessage());
    }

    @Test
    void handleUnauthorized() {
        UnauthorizedAccessException ex = new UnauthorizedAccessException("Unauthorized");
        ResponseEntity<ErrorResponse> response = handler.handleUnauthorized(ex);
        assertEquals(HttpStatus.FORBIDDEN, response.getStatusCode());
        assertEquals("Unauthorized", response.getBody().getMessage());
    }

    @Test
    void handleRentalException() {
        RentalException ex = new RentalException("Rental error");
        ResponseEntity<ErrorResponse> response = handler.handleRentalException(ex);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("Rental error", response.getBody().getMessage());
    }

    @Test
    void handleAccessDenied() {
        AccessDeniedException ex = new AccessDeniedException("Denied");
        ResponseEntity<ErrorResponse> response = handler.handleAccessDenied(ex);
        assertEquals(HttpStatus.FORBIDDEN, response.getStatusCode());
        assertEquals("Access denied. You don't have permission to perform this action.", response.getBody().getMessage());
    }

    @Test
    void handleGlobalException() {
        Exception ex = new Exception("Internal error");
        ResponseEntity<ErrorResponse> response = handler.handleGlobalException(ex);
        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertNotNull(response.getBody().getMessage());
    }
}
