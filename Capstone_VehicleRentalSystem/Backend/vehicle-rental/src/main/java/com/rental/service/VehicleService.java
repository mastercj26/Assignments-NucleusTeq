package com.rental.service;

import com.rental.dto.VehicleRequest;
import com.rental.model.Booking;
import com.rental.model.User;
import com.rental.model.Vehicle;
import com.rental.repository.BookingRepository;
import com.rental.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
@RequiredArgsConstructor
public class VehicleService {

    private final VehicleRepository vehicleRepository;
    private final BookingRepository bookingRepository;
    private final AuthService       authService;

    public List<Vehicle> getVehicles(String type, Boolean available, LocalDate startDate, LocalDate endDate) {
        User currentUser = authService.getCurrentUser();
        Vehicle.VehicleType vehicleType = parseType(type);
        Long ownerId = null;

        // If the logged-in user is a VEHICLE_OWNER, they only see their own vehicles
        if (currentUser.getRole() == User.Role.VEHICLE_OWNER) {
            ownerId = currentUser.getId();
        }

        return vehicleRepository.findFiltered(vehicleType, available, startDate, endDate, ownerId);
    }

    public Vehicle getVehicleById(Long id) {
        return vehicleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Vehicle not found with id: " + id));
    }

    public Vehicle addVehicle(VehicleRequest request) {
        Vehicle vehicle = new Vehicle();
        applyRequest(vehicle, request);
        vehicle.setOwner(authService.getCurrentUser());
        return vehicleRepository.save(vehicle);
    }

    public Vehicle updateVehicle(Long id, VehicleRequest request) {
        Vehicle vehicle = getVehicleById(id);
        User currentUser = authService.getCurrentUser();

        if (!vehicle.getOwner().getId().equals(currentUser.getId()) && !currentUser.getRole().equals(User.Role.SUPERADMIN)) {
            throw new RuntimeException("You are not authorized to update this vehicle");
        }

        applyRequest(vehicle, request);
        return vehicleRepository.save(vehicle);
    }

    public void deleteVehicle(Long id) {
        Vehicle vehicle = getVehicleById(id);
        User currentUser = authService.getCurrentUser();

        if (!vehicle.getOwner().getId().equals(currentUser.getId()) && !currentUser.getRole().equals(User.Role.SUPERADMIN)) {
            throw new RuntimeException("You are not authorized to delete this vehicle");
        }

        // Restrict deletion of booked vehicles
        if (bookingRepository.existsByVehicleIdAndStatus(id, Booking.BookingStatus.CONFIRMED)) {
            throw new RuntimeException("Cannot delete vehicle with active confirmed bookings");
        }

        vehicleRepository.delete(vehicle);
    }

    private void applyRequest(Vehicle vehicle, VehicleRequest request) {
        vehicle.setName(request.getName());
        vehicle.setType(parseRequiredType(request.getType()));
        vehicle.setDescription(request.getDescription());
        vehicle.setPricePerDay(request.getPricePerDay());
        vehicle.setIsAvailable(request.getIsAvailable() != null ? request.getIsAvailable() : true);
    }

    private Vehicle.VehicleType parseType(String type) {
        if (type == null || type.isBlank() || "ALL".equalsIgnoreCase(type)) {
            return null;
        }
        return parseRequiredType(type);
    }

    private Vehicle.VehicleType parseRequiredType(String type) {
        try {
            return Vehicle.VehicleType.valueOf(type.trim().toUpperCase());
        } catch (IllegalArgumentException | NullPointerException ex) {
            throw new RuntimeException("Vehicle type must be CAR or BIKE");
        }
    }
}
