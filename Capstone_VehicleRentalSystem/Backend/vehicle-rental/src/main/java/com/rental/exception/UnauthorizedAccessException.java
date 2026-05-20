package com.rental.exception;

public class UnauthorizedAccessException extends RentalException {
    public UnauthorizedAccessException(String message) {
        super(message);
    }
}
