package com.rental.service;

import com.rental.dto.VehicleRequest;
import com.rental.model.Vehicle;
import com.rental.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class VehicleService {

    private final VehicleRepository vehicleRepository;

    public List<Vehicle> getAllVehicles() {
        log.info("Fetching all vehicles from DB");
        return vehicleRepository.findAll();
    }

    public List<Vehicle> getAvailableVehicles() {
        return vehicleRepository.findByIsAvailableTrue();
    }

    public Vehicle getVehicleById(Long id) {
        return vehicleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Vehicle not found with id: " + id));
    }

    public Vehicle addVehicle(VehicleRequest request) {
        if (vehicleRepository.existsByVehicleNumber(request.getVehicleNumber())) {
            throw new RuntimeException(
                    "Vehicle with number " + request.getVehicleNumber() + " already exists");
        }

        Vehicle vehicle = Vehicle.builder()
                .vehicleNumber(request.getVehicleNumber())
                .name(request.getName())
                .type(Vehicle.VehicleType.valueOf(request.getType()))
                .description(request.getDescription())
                .pricePerDay(request.getPricePerDay())
                .isAvailable(request.getIsAvailable() != null ? request.getIsAvailable() : true)
                .build();

        log.info("Adding new vehicle: {} ({})", vehicle.getName(), vehicle.getVehicleNumber());
        return vehicleRepository.save(vehicle);
    }

    public Vehicle updateVehicle(Long id, VehicleRequest request) {
        Vehicle existing = getVehicleById(id);

        existing.setVehicleNumber(request.getVehicleNumber());
        existing.setName(request.getName());
        existing.setType(Vehicle.VehicleType.valueOf(request.getType()));
        existing.setDescription(request.getDescription());
        existing.setPricePerDay(request.getPricePerDay());
        existing.setIsAvailable(request.getIsAvailable());

        log.info("Updating vehicle id: {}", id);
        return vehicleRepository.save(existing);
    }

    public void deleteVehicle(Long id) {
        Vehicle existing = getVehicleById(id);
        log.info("Deleting vehicle: {} ({})", existing.getName(), existing.getVehicleNumber());
        vehicleRepository.deleteById(id);
    }
}
