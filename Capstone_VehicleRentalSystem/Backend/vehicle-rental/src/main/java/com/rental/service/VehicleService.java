package com.rental.service;

import com.rental.dto.VehicleRequest;
import com.rental.model.Vehicle;
import com.rental.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class VehicleService {

    private final VehicleRepository vehicleRepository;
    private final AuthService       authService;

    public List<Vehicle> getVehicles(String type, Boolean available) {
        Vehicle.VehicleType vehicleType = parseType(type);

        if (vehicleType != null && available != null) {
            return vehicleRepository.findByTypeAndIsAvailable(vehicleType, available);
        }
        if (vehicleType != null) {
            return vehicleRepository.findByType(vehicleType);
        }
        if (available != null) {
            return vehicleRepository.findByIsAvailable(available);
        }
        return vehicleRepository.findAll();
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

        if (!vehicle.getOwner().getId().equals(authService.getCurrentUser().getId())) {
            throw new RuntimeException("You are not authorized to update this vehicle");
        }

        applyRequest(vehicle, request);
        return vehicleRepository.save(vehicle);
    }

    public void deleteVehicle(Long id) {
        Vehicle vehicle = getVehicleById(id);

        if (!vehicle.getOwner().getId().equals(authService.getCurrentUser().getId())) {
            throw new RuntimeException("You are not authorized to delete this vehicle");
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
