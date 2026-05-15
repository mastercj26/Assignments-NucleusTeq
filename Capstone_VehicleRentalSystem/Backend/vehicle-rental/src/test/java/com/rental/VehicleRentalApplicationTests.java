package com.rental;

import com.rental.dto.AuthResponse;
import com.rental.dto.LoginRequest;
import com.rental.dto.RegisterRequest;
import com.rental.dto.VehicleRequest;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rental.model.Vehicle;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class VehicleRentalApplicationTests {

    @LocalServerPort
    private int port;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final HttpClient httpClient = HttpClient.newHttpClient();

    @Test
    void allAuthAndVehicleApiCheckpointsWork() throws Exception {
        AuthResponse registeredUser = register("Checkpoint User", "checkpoint-user@example.com", "user123");
        assertThat(registeredUser.getToken()).isNotBlank();
        assertThat(registeredUser.getRole()).isEqualTo("USER");

        AuthResponse user = login("checkpoint-user@example.com", "user123");
        AuthResponse admin = login("admin@rental.com", "admin123");
        assertThat(admin.getRole()).isEqualTo("VEHICLE_OWNER");

        HttpResponse<String> blockedVehicles = send("GET", "/api/vehicles", null, null);
        assertThat(blockedVehicles.statusCode()).isIn(HttpStatus.UNAUTHORIZED.value(), HttpStatus.FORBIDDEN.value());

        HttpResponse<String> seededVehiclesResponse = send("GET", "/api/vehicles", user.getToken(), null);
        assertThat(seededVehiclesResponse.statusCode()).isEqualTo(HttpStatus.OK.value());
        Vehicle[] seededVehicles = read(seededVehiclesResponse, Vehicle[].class);
        assertThat(seededVehicles).hasSizeGreaterThanOrEqualTo(2);

        Long firstVehicleId = seededVehicles[0].getId();
        HttpResponse<String> vehicleDetailsResponse = send("GET", "/api/vehicles/" + firstVehicleId, user.getToken(), null);
        assertThat(vehicleDetailsResponse.statusCode()).isEqualTo(HttpStatus.OK.value());
        Vehicle vehicleDetails = read(vehicleDetailsResponse, Vehicle.class);
        assertThat(vehicleDetails.getId()).isEqualTo(firstVehicleId);

        VehicleRequest newVehicle = vehicleRequest("Checkpoint Car", "CAR", "Created by API test", "2222.50", true);
        HttpResponse<String> userCannotAdd = send("POST", "/api/vehicles", user.getToken(), newVehicle);
        assertThat(userCannotAdd.statusCode()).isEqualTo(HttpStatus.FORBIDDEN.value());

        HttpResponse<String> addedResponse = send("POST", "/api/vehicles", admin.getToken(), newVehicle);
        assertThat(addedResponse.statusCode()).isEqualTo(HttpStatus.CREATED.value());
        Vehicle added = read(addedResponse, Vehicle.class);
        assertThat(added.getName()).isEqualTo("Checkpoint Car");
        Long addedId = added.getId();

        HttpResponse<String> carFilterResponse = send("GET", "/api/vehicles?type=CAR", user.getToken(), null);
        assertThat(carFilterResponse.statusCode()).isEqualTo(HttpStatus.OK.value());
        Vehicle[] carFilter = read(carFilterResponse, Vehicle[].class);
        assertThat(carFilter).allMatch(vehicle -> vehicle.getType() == Vehicle.VehicleType.CAR);

        HttpResponse<String> availableFilterResponse = send("GET", "/api/vehicles?available=true", user.getToken(), null);
        assertThat(availableFilterResponse.statusCode()).isEqualTo(HttpStatus.OK.value());
        Vehicle[] availableFilter = read(availableFilterResponse, Vehicle[].class);
        assertThat(availableFilter).allMatch(Vehicle::getIsAvailable);

        VehicleRequest updatedVehicle = vehicleRequest("Checkpoint Bike", "BIKE", "Updated by API test", "900.00", false);
        HttpResponse<String> updatedResponse = send("PUT", "/api/vehicles/" + addedId, admin.getToken(), updatedVehicle);
        assertThat(updatedResponse.statusCode()).isEqualTo(HttpStatus.OK.value());
        Vehicle updated = read(updatedResponse, Vehicle.class);
        assertThat(updated.getName()).isEqualTo("Checkpoint Bike");
        assertThat(updated.getType()).isEqualTo(Vehicle.VehicleType.BIKE);
        assertThat(updated.getIsAvailable()).isFalse();

        HttpResponse<String> combinedFilterResponse = send(
                "GET",
                "/api/vehicles?type=BIKE&available=false",
                user.getToken(),
                null
        );
        assertThat(combinedFilterResponse.statusCode()).isEqualTo(HttpStatus.OK.value());
        Vehicle[] combinedFilter = read(combinedFilterResponse, Vehicle[].class);
        assertThat(combinedFilter).anyMatch(vehicle -> vehicle.getId().equals(addedId));

        HttpResponse<String> deleted = send("DELETE", "/api/vehicles/" + addedId, admin.getToken(), null);
        assertThat(deleted.statusCode()).isEqualTo(HttpStatus.OK.value());
        assertThat(deleted.body()).contains("Vehicle deleted successfully");
    }

    private AuthResponse register(String username, String email, String password) throws Exception {
        RegisterRequest request = new RegisterRequest();
        request.setUsername(username);
        request.setEmail(email);
        request.setPassword(password);

        HttpResponse<String> response = send("POST", "/api/auth/register", null, request);

        assertThat(response.statusCode()).isEqualTo(HttpStatus.OK.value());
        return authResponse(response);
    }

    private AuthResponse login(String email, String password) throws Exception {
        LoginRequest request = new LoginRequest();
        request.setEmail(email);
        request.setPassword(password);

        HttpResponse<String> response = send("POST", "/api/auth/login", null, request);

        assertThat(response.statusCode()).isEqualTo(HttpStatus.OK.value());
        return authResponse(response);
    }

    private VehicleRequest vehicleRequest(
            String name,
            String type,
            String description,
            String pricePerDay,
            boolean isAvailable
    ) {
        VehicleRequest request = new VehicleRequest();
        request.setName(name);
        request.setType(type);
        request.setDescription(description);
        request.setPricePerDay(new BigDecimal(pricePerDay));
        request.setIsAvailable(isAvailable);
        return request;
    }

    private AuthResponse authResponse(HttpResponse<String> response) throws Exception {
        JsonNode json = objectMapper.readTree(response.body());
        return new AuthResponse(
                json.get("token").asText(),
                json.get("role").asText(),
                json.get("username").asText()
        );
    }

    private <T> T read(HttpResponse<String> response, Class<T> type) throws Exception {
        return objectMapper.readValue(response.body(), type);
    }

    private HttpResponse<String> send(String method, String path, String token, Object body) throws Exception {
        HttpRequest.Builder builder = HttpRequest.newBuilder()
                .uri(URI.create(url(path)))
                .header("Content-Type", "application/json");

        if (token != null) {
            builder.header("Authorization", "Bearer " + token);
        }

        if (body == null) {
            builder.method(method, HttpRequest.BodyPublishers.noBody());
        } else {
            builder.method(method, HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(body)));
        }

        return httpClient.send(builder.build(), HttpResponse.BodyHandlers.ofString());
    }

    private String url(String path) {
        return "http://localhost:" + port + path;
    }
}
