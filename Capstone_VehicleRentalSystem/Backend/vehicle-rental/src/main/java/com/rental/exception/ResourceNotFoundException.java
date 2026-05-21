package com.rental.exception;

public class ResourceNotFoundException extends RentalException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
