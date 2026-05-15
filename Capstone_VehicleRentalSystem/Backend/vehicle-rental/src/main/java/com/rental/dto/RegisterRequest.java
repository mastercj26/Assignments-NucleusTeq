package com.rental.dto;

import jakarta.validation.constraints.*;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RegisterRequest {
    @NotBlank
    private String username;

    @Email @NotBlank
    private String email;

    @NotBlank @Size(min = 6)
    private String password;

    private String role; // Optional, defaults to USER in service
}