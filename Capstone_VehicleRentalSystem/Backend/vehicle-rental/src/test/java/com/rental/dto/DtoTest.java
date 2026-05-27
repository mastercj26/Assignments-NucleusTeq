package com.rental.dto;

import org.junit.jupiter.api.Test;
import java.time.LocalDateTime;
import static org.junit.jupiter.api.Assertions.*;

class DtoTest {

    @Test
    void testErrorResponse() {
        ErrorResponse error = new ErrorResponse(400, "Bad Request");
        assertEquals(400, error.getStatus());
        assertEquals("Bad Request", error.getMessage());
        assertNotNull(error.getTimestamp());
        
        error.setStatus(500);
        error.setMessage("Internal Error");
        LocalDateTime now = LocalDateTime.now();
        error.setTimestamp(now);
        
        assertEquals(500, error.getStatus());
        assertEquals("Internal Error", error.getMessage());
        assertEquals(now, error.getTimestamp());
    }

    @Test
    void testBookingResponse() {
        BookingResponse response = new BookingResponse();
        response.setId(1L);
        response.setUsername("user");
        response.setVehicleName("car");
        response.setStatus("CONFIRMED");
        
        assertEquals(1L, response.getId());
        assertEquals("user", response.getUsername());
        assertEquals("car", response.getVehicleName());
        assertEquals("CONFIRMED", response.getStatus());
    }
}
