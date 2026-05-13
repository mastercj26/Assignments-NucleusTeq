package com.rental.vehicle_rental.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtUtil jwtUtil;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        // Step 1 — Read the Authorization header from the request
        String authHeader = request.getHeader("Authorization");

        // Step 2 — Check if it starts with "Bearer "
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            // No token — just continue, Spring Security will block if needed
            filterChain.doFilter(request, response);
            return;
        }

        // Step 3 — Extract the token (remove "Bearer " prefix)
        String token = authHeader.substring(7);

        // Step 4 — Validate the token
        if (!jwtUtil.isTokenValid(token)) {
            filterChain.doFilter(request, response);
            return;
        }

        // Step 5 — Extract email and role from token
        String email = jwtUtil.extractEmail(token);
        String role  = jwtUtil.extractRole(token);

        // Step 6 — Set the user in Spring Security context
        // This is how Spring knows who is making the request
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(
                        email,
                        null,
                        List.of(new SimpleGrantedAuthority("ROLE_" + role))
                        // ROLE_USER or ROLE_ADMIN
                );

        SecurityContextHolder.getContext().setAuthentication(authentication);

        // Step 7 — Continue to the actual controller
        filterChain.doFilter(request, response);
    }
}