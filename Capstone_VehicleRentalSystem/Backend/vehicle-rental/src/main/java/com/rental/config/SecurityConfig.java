package com.rental.config;

import com.rental.security.JwtAuthFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

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
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {

        http.cors(cors -> cors.configurationSource(corsConfigurationSource()));

        http.csrf(csrf -> csrf.disable());

        http.sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
        );

        http.authorizeHttpRequests(auth -> auth

                // allow preflight requests
                .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()

                // public apis
                .requestMatchers("/").permitAll()
                .requestMatchers("/api/auth/**").permitAll()

                // vehicle apis
                .requestMatchers(HttpMethod.GET, "/api/vehicles/**").authenticated()

                // booking apis
                .requestMatchers(HttpMethod.POST, "/api/bookings").authenticated()
                .requestMatchers(HttpMethod.GET, "/api/bookings")
                .hasAnyRole("VEHICLE_OWNER", "SUPERADMIN")

                .requestMatchers(HttpMethod.GET, "/api/bookings/history")
                .authenticated()

                .requestMatchers(HttpMethod.PUT, "/api/bookings/*/cancel")
                .authenticated()

                // vehicle owner and admin
                .requestMatchers(HttpMethod.POST, "/api/vehicles/**")
                .hasAnyRole("VEHICLE_OWNER", "SUPERADMIN")

                .requestMatchers(HttpMethod.PUT, "/api/vehicles/**")
                .hasAnyRole("VEHICLE_OWNER", "SUPERADMIN")

                .requestMatchers(HttpMethod.DELETE, "/api/vehicles/**")
                .hasAnyRole("VEHICLE_OWNER", "SUPERADMIN")

                // all other requests
                .anyRequest().authenticated()
        );

        // jwt filter
        http.addFilterBefore(jwtAuthFilter,
                UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {

        CorsConfiguration configuration = new CorsConfiguration();

        configuration.setAllowedOrigins(Arrays.asList("*"));

        configuration.setAllowedMethods(
                Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS")
        );

        configuration.setAllowedHeaders(
                Arrays.asList("Authorization", "Content-Type", "Accept")
        );

        configuration.setExposedHeaders(
                Arrays.asList("Authorization")
        );

        UrlBasedCorsConfigurationSource source =
                new UrlBasedCorsConfigurationSource();

        source.registerCorsConfiguration("/**", configuration);

        return source;
    }
}