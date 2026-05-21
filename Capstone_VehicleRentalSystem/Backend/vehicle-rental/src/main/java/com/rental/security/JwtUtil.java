package com.rental.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;

@Component
public class JwtUtil {

    private static final String SECRET =
            "vehicle-rental-system-secret-key-256-bit-minimum";

    private static final long EXPIRY_TIME =
            86400000L;

    private Key key =
            Keys.hmacShaKeyFor(SECRET.getBytes());

    public String generateToken(String email,
                                String role) {

        String token = Jwts.builder()
                .setSubject(email)
                .claim("role", role)
                .setIssuedAt(new Date())
                .setExpiration(
                        new Date(
                                System.currentTimeMillis()
                                        + EXPIRY_TIME
                        )
                )
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();

        return token;
    }

    public String extractEmail(String token) {

        Claims claims = getAllClaims(token);

        return claims.getSubject();
    }

    public String extractRole(String token) {

        Claims claims = getAllClaims(token);

        return claims.get("role", String.class);
    }

    public boolean isTokenValid(String token) {

        try {

            getAllClaims(token);

            return true;

        } catch (JwtException e) {

            return false;
        }
    }

    private Claims getAllClaims(String token) {

        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}