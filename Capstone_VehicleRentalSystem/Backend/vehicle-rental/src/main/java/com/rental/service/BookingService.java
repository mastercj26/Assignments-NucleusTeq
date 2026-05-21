package com.rental.service;

import com.rental.dto.BookingRequest;
import com.rental.dto.BookingResponse;
import com.rental.model.User;
import com.rental.model.Vehicle;
import com.rental.model.Vehiclebooked;
import com.rental.repository.BookingRepository;
import com.rental.repository.VehicleRepository;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class BookingService {

    private BookingRepository bookingRepository;

    private VehicleRepository vehicleRepository;

    private AuthService authService;

    public BookingService(BookingRepository bookingRepository,
                          VehicleRepository vehicleRepository,
                          AuthService authService) {

        this.bookingRepository = bookingRepository;
        this.vehicleRepository = vehicleRepository;
        this.authService = authService;
    }

    @Transactional
    public BookingResponse createBooking(BookingRequest request) {

        User user = authService.getCurrentUser();

        Vehicle vehicle = vehicleRepository.findById(
                request.getVehicleId()
        ).orElseThrow(() ->
                new RuntimeException("Vehicle not found")
        );

        if (!vehicle.getIsAvailable()) {
            throw new RuntimeException("Vehicle not available");
        }

        if (request.getEndDate().isBefore(request.getStartDate())) {
            throw new RuntimeException("Invalid booking dates");
        }

        List<Vehiclebooked> bookedVehicles =
                bookingRepository.checkVehicleBooking(
                        vehicle.getId(),
                        request.getStartDate(),
                        request.getEndDate()
                );

        if (!bookedVehicles.isEmpty()) {
            throw new RuntimeException("Vehicle already booked");
        }

        long totalDays = ChronoUnit.DAYS.between(
                request.getStartDate(),
                request.getEndDate()
        );

        if (totalDays == 0) {
            totalDays = 1;
        }

        BigDecimal totalAmount =
                vehicle.getPricePerDay().multiply(
                        BigDecimal.valueOf(totalDays)
                );

        Vehiclebooked booking = new Vehiclebooked();

        booking.setUser(user);

        booking.setVehicle(vehicle);

        booking.setStartDate(request.getStartDate());

        booking.setEndDate(request.getEndDate());

        booking.setTotalPrice(totalAmount);

        booking.setStatus(
                Vehiclebooked.BookingStatus.CONFIRMED
        );

        Vehiclebooked savedBooking =
                bookingRepository.save(booking);

        return BookingResponse.fromEntity(savedBooking);
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

        List<Vehiclebooked> bookingList;

        if (currentUser.getRole() == User.Role.VEHICLE_OWNER) {

            bookingList =
                    bookingRepository.getBookingsByOwner(
                            currentUser.getId()
                    );

        } else if (currentUser.getRole() == User.Role.SUPERADMIN) {

            bookingList = bookingRepository.findAll();

        } else {

            return getMyBookingHistory();
        }

        return bookingList.stream()
                .map(BookingResponse::fromEntity)
                .collect(Collectors.toList());
    }

    @Transactional
    public void cancelBooking(Long bookingId) {

        User user = authService.getCurrentUser();

        Vehiclebooked booking =
                bookingRepository.findById(bookingId)
                        .orElseThrow(() ->
                                new RuntimeException("Booking not found")
                        );

        boolean sameUser =
                booking.getUser().getId().equals(user.getId());

        boolean vehicleOwner =
                user.getRole() == User.Role.VEHICLE_OWNER;

        if (!sameUser && !vehicleOwner) {
            throw new RuntimeException("Cannot cancel booking");
        }

        if (booking.getStatus() ==
                Vehiclebooked.BookingStatus.CANCELLED) {

            throw new RuntimeException("Booking already cancelled");
        }

        if (booking.getStartDate().isBefore(LocalDate.now())) {

            throw new RuntimeException(
                    "Booking already started"
            );
        }

        booking.setStatus(
                Vehiclebooked.BookingStatus.CANCELLED
        );

        bookingRepository.save(booking);
    }
}