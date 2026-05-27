package com.rental.service;

import com.rental.dto.VehicleRequest;
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
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.nullable;
import static org.mockito.Mockito.*;

class VehicleServiceTest {

    @Mock
    private VehicleRepository vehicleRepository;

    @Mock
    private BookingRepository bookingRepository;

    @Mock
    private AuthService authService;

    @InjectMocks
    private VehicleService vehicleService;

    private User user;
    private Vehicle vehicle;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        user = new User();
        user.setId(1L);
        user.setRole(User.Role.USER);

        vehicle = new Vehicle();
        vehicle.setId(1L);
        vehicle.setOwner(user);
    }

    @Test
    void getVehicles_UserRole() {
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.findFiltered(any(), any(), any(), any(), any(), any())).thenReturn(Collections.emptyList());

        List<Vehicle> result = vehicleService.getVehicles("CAR", true, null, null);
        assertNotNull(result);
        verify(vehicleRepository).findFiltered(
            eq("CAR"), 
            eq(true), 
            nullable(java.time.LocalDate.class), 
            nullable(java.time.LocalDate.class), 
            nullable(Long.class), 
            eq("CONFIRMED")
        );
    }

    @Test
    void getVehicles_OwnerRole() {
        user.setRole(User.Role.VEHICLE_OWNER);
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.findFiltered(any(), any(), any(), any(), any(), any())).thenReturn(Collections.emptyList());

        vehicleService.getVehicles("ALL", null, null, null);
        verify(vehicleRepository).findFiltered(
            nullable(String.class), 
            nullable(Boolean.class), 
            nullable(java.time.LocalDate.class), 
            nullable(java.time.LocalDate.class), 
            eq(1L), 
            eq("CONFIRMED")
        );
    }

    @Test
    void getVehicleById_Success() {
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));
        Vehicle result = vehicleService.getVehicleById(1L);
        assertEquals(1L, result.getId());
    }

    @Test
    void getVehicleById_NotFound() {
        when(vehicleRepository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> vehicleService.getVehicleById(1L));
    }

    @Test
    void addVehicle_Success() {
        VehicleRequest request = new VehicleRequest("Car", "CAR", "Desc", new BigDecimal("100"), true);
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(vehicle);

        Vehicle result = vehicleService.addVehicle(request);
        assertNotNull(result);
        verify(vehicleRepository).save(any(Vehicle.class));
    }

    @Test
    void updateVehicle_Success() {
        VehicleRequest request = new VehicleRequest("Car Updated", "CAR", "Desc", new BigDecimal("120"), true);
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));
        when(authService.getCurrentUser()).thenReturn(user);
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(vehicle);

        Vehicle result = vehicleService.updateVehicle(1L, request);
        assertNotNull(result);
    }

    @Test
    void updateVehicle_Unauthorized() {
        User otherUser = new User();
        otherUser.setId(2L);
        otherUser.setRole(User.Role.USER);
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));
        when(authService.getCurrentUser()).thenReturn(otherUser);

        assertThrows(UnauthorizedAccessException.class, () -> vehicleService.updateVehicle(1L, new VehicleRequest()));
    }

    @Test
    void deleteVehicle_Success() {
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));
        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.existsByVehicleIdAndStatus(1L, Booking.BookingStatus.CONFIRMED)).thenReturn(false);

        vehicleService.deleteVehicle(1L);
        verify(vehicleRepository).delete(vehicle);
    }

    @Test
    void deleteVehicle_WithBookings() {
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(vehicle));
        when(authService.getCurrentUser()).thenReturn(user);
        when(bookingRepository.existsByVehicleIdAndStatus(1L, Booking.BookingStatus.CONFIRMED)).thenReturn(true);

        assertThrows(RentalException.class, () -> vehicleService.deleteVehicle(1L));
    }

    @Test
    void parseType_Invalid() {
        VehicleRequest request = new VehicleRequest("Car", "INVALID", "Desc", new BigDecimal("100"), true);
        when(authService.getCurrentUser()).thenReturn(user);
        assertThrows(RentalException.class, () -> vehicleService.addVehicle(request));
    }
}
