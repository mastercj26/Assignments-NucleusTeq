package com.rental.repository;

import com.rental.model.user;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface UserRepository extends JpaRepository<user, Long> {
    Optional<user> findByEmail(String email);
    Optional<user> findByUsername(String username);
    Boolean existsByEmail(String email);
}