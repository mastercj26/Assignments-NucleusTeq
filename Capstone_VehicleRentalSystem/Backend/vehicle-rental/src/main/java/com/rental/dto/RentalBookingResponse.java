package com.rental.dto;

import com.rental.model.RentalBooking;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RentalBookingResponse {
    private Long id;
    private String username;
    private String vehicleName;
    private LocalDate startDate;
    private LocalDate endDate;
    private BigDecimal totalPrice;
    private String status;

    public static RentalBookingResponse fromEntity(RentalBooking rentalBooking) {
        return new RentalBookingResponse(
                rentalBooking.getId(),
                rentalBooking.getUser().getUsername(),
                rentalBooking.getVehicle().getName(),
                rentalBooking.getStartDate(),
                rentalBooking.getEndDate(),
                rentalBooking.getTotalPrice(),
                rentalBooking.getStatus().name()
        );
    }
}
