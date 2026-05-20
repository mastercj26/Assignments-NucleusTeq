package com.rental.util;

public class Constants {
    public static final String ENDPOINT_AUTH = "/auth";
    public static final String ENDPOINT_VEHICLES = "/vehicles";
    public static final String ENDPOINT_BOOKINGS = "/bookings";
    
    public static final String ROLE_USER = "USER";
    public static final String ROLE_OWNER = "VEHICLE_OWNER";
    public static final String ROLE_ADMIN = "SUPERADMIN";

    public static final String MSG_VEHICLE_NOT_FOUND = "Vehicle not found with id: ";
    public static final String MSG_USER_NOT_FOUND = "User not found";
    public static final String MSG_BOOKING_NOT_FOUND = "Booking not found";
    public static final String MSG_UNAUTHORIZED = "You are not authorized for this action";
}
