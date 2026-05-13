package com.rental.config;

import com.rental.model.User;
import com.rental.model.Vehicle;
import com.rental.repository.UserRepository;
import com.rental.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataSeeder implements CommandLineRunner {

    private final VehicleRepository vehicleRepository;
    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        seedVehicles();
        seedUsers();
    }

    private void seedVehicles() {
        if (vehicleRepository.count() > 0) {
            log.info("Vehicles already exist in DB; skipping seed");
            return;
        }

        Vehicle car = Vehicle.builder()
                .vehicleNumber("MP09XX1234")
                .name("Honda City")
                .type(Vehicle.VehicleType.CAR)
                .description("Comfortable sedan, perfect for long trips. AC, power steering, 5 seater.")
                .pricePerDay(new BigDecimal("1500.00"))
                .isAvailable(true)
                .build();

        Vehicle bike = Vehicle.builder()
                .vehicleNumber("MP09YY5678")
                .name("Royal Enfield Classic 350")
                .type(Vehicle.VehicleType.BIKE)
                .description("Iconic cruiser bike, great for city rides and short highway trips.")
                .pricePerDay(new BigDecimal("800.00"))
                .isAvailable(true)
                .build();

        vehicleRepository.save(car);
        vehicleRepository.save(bike);

        log.info("2 sample vehicles inserted into DB successfully");
    }

    private void seedUsers() {
        if (userRepository.count() > 0) {
            log.info("Users already exist in DB; skipping seed");
            return;
        }

        User admin = User.builder()
                .username("Admin")
                .email("admin@rental.com")
                .password(passwordEncoder.encode("admin123"))
                .role(User.Role.ADMIN)
                .build();

        User user = User.builder()
                .username("John Doe")
                .email("john@rental.com")
                .password(passwordEncoder.encode("user123"))
                .role(User.Role.USER)
                .build();

        userRepository.save(admin);
        userRepository.save(user);

        log.info("Admin and User inserted into DB successfully");
        log.info("Admin login: admin@rental.com / admin123");
        log.info("User login: john@rental.com / user123");
    }
}
