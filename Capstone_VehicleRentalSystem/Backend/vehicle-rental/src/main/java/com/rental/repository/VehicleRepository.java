package com.rental.repository;

import com.rental.model.Vehicle;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    List<Vehicle> findByIsAvailableTrue();

    List<Vehicle> findByType(Vehicle.VehicleType type);

    List<Vehicle> findByTypeAndIsAvailable(
            Vehicle.VehicleType type,
            Boolean isAvailable
    );

    List<Vehicle> findByIsAvailable(Boolean isAvailable);

    List<Vehicle> findByOwnerId(Long ownerId);

    @Query("SELECT v FROM Vehicle v WHERE " +
            "(:ownerId IS NULL OR v.owner.id = :ownerId) " +
            "AND (:type IS NULL OR v.type = :type) " +
            "AND (:isAvailable IS NULL OR v.isAvailable = :isAvailable) " +
            "AND (:startDate IS NULL OR :endDate IS NULL OR v.id NOT IN (" +
            "SELECT b.vehicle.id FROM Vehiclebooked b " +
            "WHERE b.status = 'CONFIRMED' " +
            "AND b.startDate < :endDate " +
            "AND b.endDate > :startDate))")
    List<Vehicle> getFilteredVehicles(

            @Param("type") Vehicle.VehicleType type,

            @Param("isAvailable") Boolean isAvailable,

            @Param("startDate") LocalDate startDate,

            @Param("endDate") LocalDate endDate,

            @Param("ownerId") Long ownerId
    );

    @Query("SELECT v FROM Vehicle v WHERE " +
            "(:type IS NULL OR v.type = :type) " +
            "AND (:isAvailable IS NULL OR v.isAvailable = :isAvailable) " +
            "AND v.id NOT IN (" +
            "SELECT b.vehicle.id FROM Vehiclebooked b " +
            "WHERE b.status = 'CONFIRMED' " +
            "AND b.startDate < :endDate " +
            "AND b.endDate > :startDate)")
    List<Vehicle> getAvailableVehicles(

            @Param("type") Vehicle.VehicleType type,

            @Param("isAvailable") Boolean isAvailable,

            @Param("startDate") LocalDate startDate,

            @Param("endDate") LocalDate endDate
    );
}