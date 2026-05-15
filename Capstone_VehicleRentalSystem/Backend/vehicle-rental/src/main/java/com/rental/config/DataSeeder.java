package com.rental.config;

import com.rental.model.User;
import com.rental.model.Vehicle;
import com.rental.repository.UserRepository;
import com.rental.repository.VehicleRepository;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

@Component
@RequiredArgsConstructor
public class DataSeeder implements CommandLineRunner {

    private final UserRepository userRepository;
    private final VehicleRepository vehicleRepository;
    private final BCryptPasswordEncoder passwordEncoder;
    private final EntityManager entityManager;

    @Override
    @Transactional
    public void run(String... args) {
        fixRoleConfusion();
        seedUsers();
        seedVehicles();
    }

    private void fixRoleConfusion() {
        // 1. Drop the old constraint that only allowed 'USER' and 'ADMIN'
        entityManager.createNativeQuery("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check")
                .executeUpdate();

        // 2. Update existing 'ADMIN' to 'VEHICLE_OWNER'
        entityManager.createNativeQuery("UPDATE users SET role = 'VEHICLE_OWNER' WHERE role = 'ADMIN'")
                .executeUpdate();

        // 3. Assign an owner to existing vehicles that don't have one (orphaned data)
        User admin = userRepository.findByEmail("admin@rental.com").orElse(null);
        if (admin != null) {
            entityManager.createNativeQuery("UPDATE vehicles SET owner_id = :ownerId WHERE owner_id IS NULL")
                    .setParameter("ownerId", admin.getId())
                    .executeUpdate();
        }
    }

    private void seedUsers() {
        if (!userRepository.existsByEmail("admin@rental.com")) {
            User admin = new User();
            admin.setUsername("Admin");
            admin.setEmail("admin@rental.com");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setRole(User.Role.VEHICLE_OWNER);
            userRepository.save(admin);
        }

        if (!userRepository.existsByEmail("john@rental.com")) {
            User user = new User();
            user.setUsername("John Doe");
            user.setEmail("john@rental.com");
            user.setPassword(passwordEncoder.encode("user123"));
            user.setRole(User.Role.USER);
            userRepository.save(user);
        }
    }

    private void seedVehicles() {
        if (vehicleRepository.count() > 0) {
            return;
        }

        User admin = userRepository.findByEmail("admin@rental.com").orElse(null);

        // --- CARS ---
        saveVehicle("Honda City", Vehicle.VehicleType.CAR, 
            "Comfortable sedan with AC, power steering, and five seats.", 1500.00, true, admin);
        
        saveVehicle("Toyota Fortuner", Vehicle.VehicleType.CAR, 
            "Powerful 7-seater SUV, perfect for family trips and off-roading.", 4500.00, true, admin);
        
        saveVehicle("Hyundai i20", Vehicle.VehicleType.CAR, 
            "Premium hatchback with great mileage and easy city driving.", 1200.00, true, admin);

        saveVehicle("Mercedes Benz C-Class", Vehicle.VehicleType.CAR, 
            "Luxury sedan for business meetings and special occasions.", 8500.00, false, admin);

        // --- BIKES ---
        saveVehicle("Royal Enfield Classic 350", Vehicle.VehicleType.BIKE, 
            "Iconic cruiser bike for city rides and highway trips.", 800.00, true, admin);
        
        saveVehicle("KTM Duke 390", Vehicle.VehicleType.BIKE, 
            "High-performance sports bike for speed enthusiasts.", 1100.00, true, admin);
        
        saveVehicle("Honda Activa 6G", Vehicle.VehicleType.BIKE, 
            "Convenient gearless scooter for quick city errands.", 400.00, true, admin);

        saveVehicle("Harley Davidson Iron 883", Vehicle.VehicleType.BIKE, 
            "Premium cruiser for the ultimate riding experience.", 3500.00, false, admin);
    }

    private void saveVehicle(String name, Vehicle.VehicleType type, String desc, double price, boolean available, User owner) {
        Vehicle v = new Vehicle();
        v.setName(name);
        v.setType(type);
        v.setDescription(desc);
        v.setPricePerDay(new BigDecimal(price));
        v.setIsAvailable(available);
        v.setOwner(owner);
        vehicleRepository.save(v);
    }
}
