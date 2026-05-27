package com.rental.controller;

import com.rental.dto.BookingRequest;
import com.rental.dto.BookingResponse;
import com.rental.service.BookingService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class BookingControllerTest {

    @Mock
    private BookingService bookingService;

    @InjectMocks
    private BookingController bookingController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void createBooking_Success() {
        BookingRequest request = new BookingRequest();
        BookingResponse fakeResponse = new BookingResponse();
        when(bookingService.createBooking(any(BookingRequest.class))).thenReturn(fakeResponse);

        ResponseEntity<BookingResponse> response = bookingController.createBooking(request);

        assertNotNull(response);
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        verify(bookingService, times(1)).createBooking(request);
    }

    @Test
    void getAllBookings_Success() {
        when(bookingService.getAllBookings()).thenReturn(Collections.emptyList());

        ResponseEntity<List<BookingResponse>> response = bookingController.getAllBookings();

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(bookingService, times(1)).getAllBookings();
    }

    @Test
    void getBookingHistory_Success() {
        when(bookingService.getMyBookingHistory()).thenReturn(Collections.emptyList());

        ResponseEntity<List<BookingResponse>> response = bookingController.getBookingHistory();

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        verify(bookingService, times(1)).getMyBookingHistory();
    }

    @Test
    void cancelBooking_Success() {
        doNothing().when(bookingService).cancelBooking(1L);

        ResponseEntity<String> response = bookingController.cancelBooking(1L);

        assertNotNull(response);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("Booking cancelled successfully", response.getBody());
        verify(bookingService, times(1)).cancelBooking(1L);
    }
}
