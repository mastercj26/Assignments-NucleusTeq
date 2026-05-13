package com.rental.config;

import com.rental.security.JwtAuthFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthFilter jwtAuthFilter;

    @Bean
    public BCryptPasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .sessionManagement(session ->
                        session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth

                        // ── PUBLIC endpoints — no token needed ──
                        .requestMatchers("/api/auth/**").permitAll()

                        // ── ADMIN only endpoints ──
                        .requestMatchers("/api/vehicles").authenticated()
                        .requestMatchers("/api/vehicles/**").authenticated()
                        .requestMatchers("/api/bookings").hasRole("ADMIN")

                        // ── USER + ADMIN endpoints ──
                        .requestMatchers("/api/bookings/my").authenticated()
                        .requestMatchers("/api/bookings/**").authenticated()

                        // ── Everything else needs login ──
                        .anyRequest().authenticated()
                )
                // Add our JWT filter BEFORE Spring's default filter
                .addFilterBefore(jwtAuthFilter,
                        UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
