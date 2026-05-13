package com.rental.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.math.BigDecimal;

@Data
public class VehicleRequest {

    @NotBlank(message = "Vehicle number is required")
    private String vehicleNumber;

    @NotBlank(message = "Vehicle name is required")
    private String name;

    @NotNull(message = "Vehicle type is required")
    private String type;

    private String description;

    @NotNull(message = "Price per day is required")
    private BigDecimal pricePerDay;

    private Boolean isAvailable = true;
}
