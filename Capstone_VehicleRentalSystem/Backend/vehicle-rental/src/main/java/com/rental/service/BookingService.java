package com.rental.service;

import com.rental.dto.BookingRequest;
import com.rental.dto.BookingResponse;
import com.rental.model.Booking;
import com.rental.model.User;
import com.rental.model.Vehicle;
import com.rental.repository.BookingRepository;
import com.rental.repository.VehicleRepository;
import com.rental.exception.RentalException;
import com.rental.exception.ResourceNotFoundException;
import com.rental.exception.UnauthorizedAccessException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class BookingService {

    private final BookingRepository bookingRepository;
    private final VehicleRepository vehicleRepository;
    private final AuthService       authService;

    @Transactional
    public BookingResponse createBooking(BookingRequest request) {
        User user = authService.getCurrentUser();
        Vehicle vehicle = vehicleRepository.findById(request.getVehicleId())
                .orElseThrow(() -> new ResourceNotFoundException("Vehicle not found with id: " + request.getVehicleId()));

        if (!vehicle.getIsAvailable()) {
            throw new RentalException("Vehicle is currently not available for rent");
        }

        if (request.getEndDate().isBefore(request.getStartDate())) {
            throw new RentalException("End date cannot be before start date");
        }

        // --- Overlap Validation Logic (CRITICAL) ---
        List<Booking> overlapping = bookingRepository.findOverlappingBookings(
                vehicle.getId(), request.getStartDate(), request.getEndDate()
        );

        if (!overlapping.isEmpty()) {
            throw new RentalException("Vehicle is already booked for the selected dates");
        }

        // Calculate Total Price
        long days = ChronoUnit.DAYS.between(request.getStartDate(), request.getEndDate());
        if (days <= 0) days = 1; // Minimum 1 day charge
        BigDecimal total = vehicle.getPricePerDay().multiply(BigDecimal.valueOf(days));

        Booking booking = new Booking();
        booking.setUser(user);
        booking.setVehicle(vehicle);
        booking.setStartDate(request.getStartDate());
        booking.setEndDate(request.getEndDate());
        booking.setTotalPrice(total);
        booking.setStatus(Booking.BookingStatus.CONFIRMED);

        return BookingResponse.fromEntity(bookingRepository.save(booking));
    }

    public List<BookingResponse> getMyBookingHistory() {
        User user = authService.getCurrentUser();
        return bookingRepository.findByUserId(user.getId())
                .stream()
                .map(BookingResponse::fromEntity)
                .collect(Collectors.toList());
    }

    public List<BookingResponse> getAllBookings() {
        User currentUser = authService.getCurrentUser();
        List<Booking> bookings;

        if (currentUser.getRole() == User.Role.VEHICLE_OWNER) {
            bookings = bookingRepository.findByVehicleOwnerId(currentUser.getId());
        } else if (currentUser.getRole() == User.Role.SUPERADMIN) {
            bookings = bookingRepository.findAll();
        } else {
            // Regular users shouldn't really be calling getAllBookings (it's protected by PreAuthorize)
            // but for safety, return empty or their own history
            return getMyBookingHistory();
        }

        return bookings.stream()
                .map(BookingResponse::fromEntity)
                .collect(Collectors.toList());
    }

    @Transactional
    public void cancelBooking(Long bookingId) {
        User user = authService.getCurrentUser();
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + bookingId));

        // Check if user is owner or VEHICLE_OWNER
        if (!booking.getUser().getId().equals(user.getId()) && !user.getRole().equals(User.Role.VEHICLE_OWNER)) {
            throw new UnauthorizedAccessException("Unauthorized to cancel this booking");
        }

        if (booking.getStatus() == Booking.BookingStatus.CANCELLED) {
            throw new RentalException("Booking is already cancelled");
        }

        if (booking.getStartDate().isBefore(LocalDate.now())) {
            throw new RentalException("Cannot cancel a booking that has already started");
        }

        booking.setStatus(Booking.BookingStatus.CANCELLED);
        bookingRepository.save(booking);
    }
}
