package com.rental.repository;

import com.rental.model.vehicle;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface VehicleRepository extends JpaRepository<vehicle, Long> {
    List<vehicle> findByIsAvailableTrue();
    List<vehicle> findByType(vehicle.VehicleType type);
}