package com.rental.repository;

import com.rental.model.RentalBooking;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface RentalBookingRepository extends JpaRepository<RentalBooking, Long> {

    List<RentalBooking> findByUserId(Long userId);

    @Query("SELECT b FROM RentalBooking b WHERE b.vehicle.owner.id = :ownerId")
    List<RentalBooking> getBookingsByOwnerId(@Param("ownerId") Long ownerId);

    @Query("SELECT b FROM RentalBooking b WHERE " +
            "b.vehicle.id = :vehicleId " +
            "AND b.status = 'CONFIRMED' " +
            "AND b.startDate < :endDate " +
            "AND b.endDate > :startDate")
    List<RentalBooking> checkBookingDates(
            @Param("vehicleId") Long vehicleId,
            @Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate
    );

    boolean existsByVehicleIdAndStatus(
            Long vehicleId,
            RentalBooking.BookingStatus status
    );
}