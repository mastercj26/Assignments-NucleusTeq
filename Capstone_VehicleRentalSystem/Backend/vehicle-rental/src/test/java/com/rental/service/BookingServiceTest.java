package com.rental.service;

import com.rental.dto.BookingRequest;
import com.rental.dto.BookingResponse;
import com.rental.exception.RentalException;
import com.rental.exception.ResourceNotFoundException;
import com.rental.exception.UnauthorizedAccessException;
import com.rental.model.Booking;
import com.rental.model.User;
import com.rental.model.Vehicle;
import com.rental.repository.BookingRepository;
import com.rental.repository.VehicleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class BookingServiceTest {

    @Mock
    private BookingRepository bookingRepository;

    @Mock
    private VehicleRepository vehicleRepository;

    @Mock
    private AuthService authService;

    @InjectMocks
    private BookingService bookingService;

    private User user;
    private Vehicle vehicle;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        user = new User();
        user.setId(1L);
        user.setEmail("user@example.com");
        user.setUsername("testuser");
        user.setRole(User.Role.USER);

        vehicle = new Vehicle();
        vehicle.setId(1L);
        vehicle.setName("Test Car");
        vehicle.setIsAvailable(true);
        vehicle.setPricePerDay(new BigDecimal("100.00"));
    }

    @Test
    void createBooking_Success() {
        BookingRequest request = new BookingRequest(1L, LocalDate.now().plusDays(1), LocalDate.now().plusDays(3));
        
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));
        when(bookingRepository.findOverlappingBookings(any(), any(), any(), any())).thenReturn(Collections.emptyList());
        
        Booking savedBooking = new Booking();
        savedBooking.setId(10L);
        savedBooking.setUser(user);
        savedBooking.setVehicle(vehicle);
        savedBooking.setStartDate(request.getStartDate());
        savedBooking.setEndDate(request.getEndDate());
        savedBooking.setTotalPrice(new BigDecimal("200.00"));
        savedBooking.setStatus(Booking.BookingStatus.CONFIRMED);
        
        when(bookingRepository.save(any(Booking.class))).thenReturn(savedBooking);

        BookingResponse response = bookingService.createBooking(request);

        assertNotNull(response);
        assertEquals(10L, response.getId());
        assertEquals("CONFIRMED", response.getStatus());
        verify(bookingRepository, times(1)).save(any(Booking.class));
    }

    @Test
    void createBooking_VehicleNotFound() {
        BookingRequest request = new BookingRequest(1L, LocalDate.now(), LocalDate.now().plusDays(1));
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> bookingService.createBooking(request));
    }

    @Test
    void createBooking_VehicleNotAvailable() {
        BookingRequest request = new BookingRequest(1L, LocalDate.now(), LocalDate.now().plusDays(1));
        vehicle.setIsAvailable(false);
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));

        assertThrows(RentalException.class, () -> bookingService.createBooking(request));
    }

    @Test
    void createBooking_InvalidDates() {
        BookingRequest request = new BookingRequest(1L, LocalDate.now().plusDays(2), LocalDate.now().plusDays(1));
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));

        assertThrows(RentalException.class, () -> bookingService.createBooking(request));
    }

    @Test
    void createBooking_Overlapping() {
        BookingRequest request = new BookingRequest(1L, LocalDate.now(), LocalDate.now().plusDays(1));
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));
        when(bookingRepository.findOverlappingBookings(any(), any(), any(), any())).thenReturn(List.of(new Booking()));

        assertThrows(RentalException.class, () -> bookingService.createBooking(request));
    }

    @Test
    void getMyBookingHistory_Success() {
        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findByUserId(1L)).thenReturn(Collections.emptyList());

        List<BookingResponse> responses = bookingService.getMyBookingHistory();
        assertNotNull(responses);
        assertTrue(responses.isEmpty());
    }

    @Test
    void getAllBookings_SuperAdmin() {
        user.setRole(User.Role.SUPERADMIN);
        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findAll()).thenReturn(Collections.emptyList());

        List<BookingResponse> responses = bookingService.getAllBookings();
        assertNotNull(responses);
        verify(bookingRepository, times(1)).findAll();
    }

    @Test
    void getAllBookings_VehicleOwner() {
        user.setRole(User.Role.VEHICLE_OWNER);
        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findByVehicleOwnerId(user.getId())).thenReturn(Collections.emptyList());

        List<BookingResponse> responses = bookingService.getAllBookings();
        assertNotNull(responses);
        verify(bookingRepository, times(1)).findByVehicleOwnerId(user.getId());
    }

    @Test
    void getAllBookings_RegularUser() {
        user.setRole(User.Role.USER);
        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findByUserId(user.getId())).thenReturn(Collections.emptyList());

        List<BookingResponse> responses = bookingService.getAllBookings();
        assertNotNull(responses);
        verify(bookingRepository, times(1)).findByUserId(user.getId());
    }

    @Test
    void cancelBooking_Success() {
        Booking booking = new Booking();
        booking.setId(10L);
        booking.setUser(user);
        booking.setStartDate(LocalDate.now().plusDays(1));
        booking.setStatus(Booking.BookingStatus.CONFIRMED);

        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(booking));

        bookingService.cancelBooking(10L);

        assertEquals(Booking.BookingStatus.CANCELLED, booking.getStatus());
        verify(bookingRepository, times(1)).save(booking);
    }

    @Test
    void cancelBooking_NotFound() {
        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findById(10L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> bookingService.cancelBooking(10L));
    }

    @Test
    void cancelBooking_Unauthorized() {
        User otherUser = new User();
        otherUser.setId(2L);
        Booking booking = new Booking();
        booking.setUser(otherUser);

        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(booking));

        assertThrows(UnauthorizedAccessException.class, () -> bookingService.cancelBooking(10L));
    }

    @Test
    void cancelBooking_AlreadyCancelled() {
        Booking booking = new Booking();
        booking.setUser(user);
        booking.setStatus(Booking.BookingStatus.CANCELLED);
        booking.setStartDate(LocalDate.now().plusDays(1));

        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(booking));

        assertThrows(RentalException.class, () -> bookingService.cancelBooking(10L));
    }

    @Test
    void cancelBooking_AlreadyStarted() {
        Booking booking = new Booking();
        booking.setUser(user);
        booking.setStatus(Booking.BookingStatus.CONFIRMED);
        booking.setStartDate(LocalDate.now().minusDays(1));

        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(booking));

        assertThrows(RentalException.class, () -> bookingService.cancelBooking(10L));
    }
}
