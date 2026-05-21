package com.rental.dto;

import com.rental.model.Vehiclebooked;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BookingResponse {
    private Long id;
    private String username;
    private String vehicleName;
    private LocalDate startDate;
    private LocalDate endDate;
    private BigDecimal totalPrice;
    private String status;

    public static BookingResponse fromEntity(Vehiclebooked booking) {
        return new BookingResponse(
                booking.getId(),
                booking.getUser().getUsername(),
                booking.getVehicle().getName(),
                booking.getStartDate(),
                booking.getEndDate(),
                booking.getTotalPrice(),
                booking.getStatus().name()
        );
    }
}
