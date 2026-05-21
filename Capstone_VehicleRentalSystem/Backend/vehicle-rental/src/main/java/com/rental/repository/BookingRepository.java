package com.rental.repository;

import com.rental.model.Vehiclebooked;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface BookingRepository extends JpaRepository<Vehiclebooked, Long> {

    List<Vehiclebooked> findByUserId(Long userId);

    @Query("SELECT b FROM Vehiclebooked b WHERE b.vehicle.owner.id = :ownerId")
    List<Vehiclebooked> getBookingsByOwner(@Param("ownerId") Long ownerId);

    @Query("SELECT b FROM Vehiclebooked b WHERE " +
            "b.vehicle.id = :vehicleId " +
            "AND b.status = 'CONFIRMED' " +
            "AND b.startDate < :endDate " +
            "AND b.endDate > :startDate")
    List<Vehiclebooked> checkVehicleBooking(
            @Param("vehicleId") Long vehicleId,
            @Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate
    );

    boolean existsByVehicleIdAndStatus(
            Long vehicleId,
            Vehiclebooked.BookingStatus status
    );
}