package com.rental.repository;

import com.rental.model.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface VehicleRepository extends JpaRepository<Vehicle, Long> {
    List<Vehicle> findByIsAvailableTrue();
    List<Vehicle> findByType(Vehicle.VehicleType type);
}
