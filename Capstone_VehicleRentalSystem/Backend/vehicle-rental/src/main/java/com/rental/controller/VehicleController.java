package com.rental.controller;

import com.rental.dto.VehicleRequest;
import com.rental.model.Vehicle;
import com.rental.service.VehicleService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/vehicles")
@CrossOrigin(origins = "*")
public class VehicleController {

    @Autowired
    private VehicleService vehicleService;

    @GetMapping
    public ResponseEntity<List<Vehicle>> getVehicles(
            @RequestParam(required = false) String type,
            @RequestParam(required = false) Boolean available,
            @RequestParam(required = false) LocalDate startDate,
            @RequestParam(required = false) LocalDate endDate) {
        List<Vehicle> vehicles = vehicleService.getVehicles(type, available, startDate, endDate);
        return ResponseEntity.ok(vehicles);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Vehicle> getVehicle(@PathVariable Long id) {
        Vehicle vehicle = vehicleService.getVehicleById(id);
        return ResponseEntity.ok(vehicle);
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('VEHICLE_OWNER', 'SUPERADMIN')")
    public ResponseEntity<Vehicle> addVehicle(@Valid @RequestBody VehicleRequest request) {
        Vehicle newVehicle = vehicleService.addVehicle(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(newVehicle);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('VEHICLE_OWNER', 'SUPERADMIN')")
    public ResponseEntity<Vehicle> updateVehicle(@PathVariable Long id, @Valid @RequestBody VehicleRequest request) {
        Vehicle updatedVehicle = vehicleService.updateVehicle(id, request);
        return ResponseEntity.ok(updatedVehicle);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyRole('VEHICLE_OWNER', 'SUPERADMIN')")
    public ResponseEntity<String> deleteVehicle(@PathVariable Long id) {
        vehicleService.deleteVehicle(id);
        return ResponseEntity.ok("Vehicle deleted successfully");
    }
}