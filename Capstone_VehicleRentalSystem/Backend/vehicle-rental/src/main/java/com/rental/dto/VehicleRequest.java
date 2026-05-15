package com.rental.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class VehicleRequest {

    @NotBlank(message = "Vehicle name is required")
    private String name;

    @NotNull(message = "Vehicle type is required")
    private String type;

    private String description;

    @NotNull(message = "Price per day is required")
    private BigDecimal pricePerDay;

    private Boolean isAvailable = true;
}
