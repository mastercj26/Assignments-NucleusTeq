package com.rental.repository;

import com.rental.model.Booking;
import com.rental.model.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    List<Vehicle> findByIsAvailableTrue();
    List<Vehicle> findByType(Vehicle.VehicleType type);
    List<Vehicle> findByTypeAndIsAvailable(Vehicle.VehicleType type, Boolean isAvailable);
    List<Vehicle> findByIsAvailable(Boolean isAvailable);
    List<Vehicle> findByOwnerId(Long ownerId);

    @Query(value = """
        SELECT v.* FROM vehicles v
        WHERE (:ownerId IS NULL OR v.owner_id = :ownerId)
        AND (:type IS NULL OR v.type = CAST(:type AS VARCHAR))
        AND (:isAvailable IS NULL OR v.is_available = :isAvailable)
        AND (
            CAST(:startDate AS DATE) IS NULL
            OR CAST(:endDate AS DATE) IS NULL
            OR NOT EXISTS (
                SELECT 1 FROM bookings b
                WHERE b.vehicle_id = v.id
                AND b.status = CAST(:status AS VARCHAR)
                AND b.start_date < CAST(:endDate AS DATE)
                AND b.end_date > CAST(:startDate AS DATE)
            )
        )
        """, nativeQuery = true)
    List<Vehicle> findFiltered(
            @Param("type") String type,
            @Param("isAvailable") Boolean isAvailable,
            @Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate,
            @Param("ownerId") Long ownerId,
            @Param("status") String status
    );
}