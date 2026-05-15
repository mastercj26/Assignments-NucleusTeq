package com.rental.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.util.List;

@Entity
@Table(name = "vehicles")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private VehicleType type;       // CAR or BIKE

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(name = "price_per_day", precision = 8, scale = 2)
    private BigDecimal pricePerDay;

    @Column(name = "is_available", nullable = false)
    private Boolean isAvailable = true;

    @ManyToOne
    @JoinColumn(name = "owner_id")
    private User owner;

    @OneToMany(mappedBy = "vehicle", cascade = CascadeType.ALL)
    @JsonIgnore
    private List<Booking> bookings;

    public enum VehicleType { CAR, BIKE }
}
