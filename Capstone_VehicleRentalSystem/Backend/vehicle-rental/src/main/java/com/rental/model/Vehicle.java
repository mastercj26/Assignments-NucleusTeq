package com.rental.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.List;

@Entity
@Table(name = "vehicles")
public class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false , length = 100)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private VehicleType type;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(name = "price_per_day" , precision = 8 , scale = 2)
    private BigDecimal pricePerDay;

    @Column(name = "is_available" , nullable = false)
    private Boolean isAvailable = true;

    @ManyToOne
    @JoinColumn(name = "owner_id")
    private User owner;

    @OneToMany(mappedBy = "vehicle" , cascade = CascadeType.ALL)
    @JsonIgnore
    private List<Vehiclebooked> bookings;

    public Vehicle() {
    }

    public Vehicle(Long id, String name, VehicleType type, String description,
                   BigDecimal pricePerDay, Boolean isAvailable,
                   User owner, List<Vehiclebooked> bookings) {

        this.id = id;
        this.name = name;
        this.type = type;
        this.description = description;
        this.pricePerDay = pricePerDay;
        this.isAvailable = isAvailable;
        this.owner = owner;
        this.bookings = bookings;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public VehicleType getType() {
        return type;
    }

    public void setType(VehicleType type) {
        this.type = type;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public BigDecimal getPricePerDay() {
        return pricePerDay;
    }

    public void setPricePerDay(BigDecimal pricePerDay) {
        this.pricePerDay = pricePerDay;
    }

    public Boolean getIsAvailable() {
        return isAvailable;
    }

    public void setIsAvailable(Boolean available) {
        isAvailable = available;
    }

    public User getOwner() {
        return owner;
    }

    public void setOwner(User owner) {
        this.owner = owner;
    }

    public List<Vehiclebooked> getBookings() {
        return bookings;
    }

    public void setBookings(List<Vehiclebooked> bookings) {
        this.bookings = bookings;
    }

    public enum VehicleType {
        CAR,
        BIKE
    }
}