package com.rental.service;

import com.rental.dto.VehicleRequest;
import com.rental.model.User;
import com.rental.model.Vehicle;
import com.rental.model.Vehiclebooked;
import com.rental.repository.BookingRepository;
import com.rental.repository.VehicleRepository;

import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class VehicleService {

    private VehicleRepository vehicleRepository;

    private BookingRepository bookingRepository;

    private AuthService authService;

    public VehicleService(VehicleRepository vehicleRepository,
                          BookingRepository bookingRepository,
                          AuthService authService) {

        this.vehicleRepository = vehicleRepository;
        this.bookingRepository = bookingRepository;
        this.authService = authService;
    }

    public List<Vehicle> getVehicles(String type,
                                     Boolean available,
                                     LocalDate startDate,
                                     LocalDate endDate) {

        User currentUser = authService.getCurrentUser();

        Vehicle.VehicleType vehicleType = convertType(type);

        Long ownerId = null;

        if (currentUser.getRole() == User.Role.VEHICLE_OWNER) {
            ownerId = currentUser.getId();
        }

        return vehicleRepository.getFilteredVehicles(
                vehicleType,
                available,
                startDate,
                endDate,
                ownerId
        );
    }

    public Vehicle getVehicleById(Long id) {

        return vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new RuntimeException("Vehicle not found"));
    }

    public Vehicle addVehicle(VehicleRequest request) {

        Vehicle vehicle = new Vehicle();

        setVehicleData(vehicle, request);

        vehicle.setOwner(authService.getCurrentUser());

        return vehicleRepository.save(vehicle);
    }

    public Vehicle updateVehicle(Long id, VehicleRequest request) {

        Vehicle vehicle = getVehicleById(id);

        User currentUser = authService.getCurrentUser();

        boolean isOwner =
                vehicle.getOwner().getId().equals(currentUser.getId());

        boolean isAdmin =
                currentUser.getRole() == User.Role.SUPERADMIN;

        if (!isOwner && !isAdmin) {
            throw new RuntimeException("You cannot update this vehicle");
        }

        setVehicleData(vehicle, request);

        return vehicleRepository.save(vehicle);
    }

    public void deleteVehicle(Long id) {

        Vehicle vehicle = getVehicleById(id);

        User currentUser = authService.getCurrentUser();

        boolean isOwner =
                vehicle.getOwner().getId().equals(currentUser.getId());

        boolean isAdmin =
                currentUser.getRole() == User.Role.SUPERADMIN;

        if (!isOwner && !isAdmin) {
            throw new RuntimeException("You cannot delete this vehicle");
        }

        boolean bookingExists =
                bookingRepository.existsByVehicleIdAndStatus(
                        id,
                        Vehiclebooked.BookingStatus.CONFIRMED
                );

        if (bookingExists) {
            throw new RuntimeException("Vehicle already booked");
        }

        vehicleRepository.delete(vehicle);
    }

    private void setVehicleData(Vehicle vehicle,
                                VehicleRequest request) {

        vehicle.setName(request.getName());

        vehicle.setType(getVehicleType(request.getType()));

        vehicle.setDescription(request.getDescription());

        vehicle.setPricePerDay(request.getPricePerDay());

        if (request.getIsAvailable() != null) {
            vehicle.setIsAvailable(request.getIsAvailable());
        } else {
            vehicle.setIsAvailable(true);
        }
    }

    private Vehicle.VehicleType convertType(String type) {

        if (type == null || type.trim().isEmpty()) {
            return null;
        }

        if (type.equalsIgnoreCase("ALL")) {
            return null;
        }

        return getVehicleType(type);
    }

    private Vehicle.VehicleType getVehicleType(String type) {

        try {

            return Vehicle.VehicleType.valueOf(
                    type.toUpperCase()
            );

        } catch (Exception e) {

            throw new RuntimeException(
                    "Type should be CAR or BIKE"
            );
        }
    }
}