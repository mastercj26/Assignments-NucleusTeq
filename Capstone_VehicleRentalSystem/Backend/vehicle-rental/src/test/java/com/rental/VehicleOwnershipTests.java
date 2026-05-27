package com.rental;

import com.rental.dto.AuthResponse;
import com.rental.dto.RegisterRequest;
import com.rental.dto.VehicleRequest;
import com.rental.model.Vehicle;
import com.fasterxml.jackson.databind.ObjectMapper;
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
class VehicleOwnershipTests {

    @LocalServerPort
    private int port;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final HttpClient httpClient = HttpClient.newHttpClient();

    @Test
    void ownersShouldOnlySeeTheirOwnVehicles() throws Exception {
        // 1. Register two owners
        AuthResponse owner1 = register("Owner One", "owner1@example.com", "pass123", "VEHICLE_OWNER");
        AuthResponse owner2 = register("Owner Two", "owner2@example.com", "pass123", "VEHICLE_OWNER");
        AuthResponse user = register("Regular User", "user@example.com", "pass123", "USER");

        // 2. Owner 1 adds a vehicle
        VehicleRequest v1Req = vehicleRequest("Owner 1 Car", "CAR", "O1 Car", "1000", true);
        HttpResponse<String> v1Resp = send("POST", "/v1/vehicles", owner1.getToken(), v1Req);
        assertThat(v1Resp.statusCode()).isEqualTo(HttpStatus.CREATED.value());
        Vehicle v1 = objectMapper.readValue(v1Resp.body(), Vehicle.class);

        // 3. Owner 2 adds a vehicle
        VehicleRequest v2Req = vehicleRequest("Owner 2 Bike", "BIKE", "O2 Bike", "500", true);
        HttpResponse<String> v2Resp = send("POST", "/v1/vehicles", owner2.getToken(), v2Req);
        assertThat(v2Resp.statusCode()).isEqualTo(HttpStatus.CREATED.value());
        Vehicle v2 = objectMapper.readValue(v2Resp.body(), Vehicle.class);

        // 4. Owner 1 lists vehicles - should only see their own
        HttpResponse<String> listO1Resp = send("GET", "/v1/vehicles", owner1.getToken(), null);
        Vehicle[] listO1 = objectMapper.readValue(listO1Resp.body(), Vehicle[].class);
        assertThat(listO1).allMatch(v -> v.getOwner().getUsername().equals("Owner One"));
        assertThat(listO1).anyMatch(v -> v.getId().equals(v1.getId()));
        assertThat(listO1).noneMatch(v -> v.getId().equals(v2.getId()));

        // 5. Owner 2 lists vehicles - should only see their own
        HttpResponse<String> listO2Resp = send("GET", "/v1/vehicles", owner2.getToken(), null);
        Vehicle[] listO2 = objectMapper.readValue(listO2Resp.body(), Vehicle[].class);
        assertThat(listO2).allMatch(v -> v.getOwner().getUsername().equals("Owner Two"));
        assertThat(listO2).anyMatch(v -> v.getId().equals(v2.getId()));
        assertThat(listO2).noneMatch(v -> v.getId().equals(v1.getId()));

        // 6. Regular user lists vehicles - should see both
        HttpResponse<String> listUserResp = send("GET", "/v1/vehicles", user.getToken(), null);
        Vehicle[] listUser = objectMapper.readValue(listUserResp.body(), Vehicle[].class);
        assertThat(listUser).anyMatch(v -> v.getId().equals(v1.getId()));
        assertThat(listUser).anyMatch(v -> v.getId().equals(v2.getId()));
    }

    private AuthResponse register(String username, String email, String password, String role) throws Exception {
        RegisterRequest request = new RegisterRequest();
        request.setUsername(username);
        request.setEmail(email);
        request.setPassword(password);
        request.setRole(role);

        HttpResponse<String> response = send("POST", "/v1/auth/register", null, request);
        assertThat(response.statusCode()).isEqualTo(HttpStatus.OK.value());
        
        var json = objectMapper.readTree(response.body());
        return new AuthResponse(
                json.get("token").asText(),
                json.get("role").asText(),
                json.get("username").asText()
        );
    }

    private VehicleRequest vehicleRequest(String name, String type, String desc, String price, boolean avail) {
        VehicleRequest req = new VehicleRequest();
        req.setName(name);
        req.setType(type);
        req.setDescription(desc);
        req.setPricePerDay(new BigDecimal(price));
        req.setIsAvailable(avail);
        return req;
    }

    private HttpResponse<String> send(String method, String path, String token, Object body) throws Exception {
        HttpRequest.Builder builder = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:" + port + path))
                .header("Content-Type", "application/json");
        if (token != null) builder.header("Authorization", "Bearer " + token);
        if (body == null) builder.method(method, HttpRequest.BodyPublishers.noBody());
        else builder.method(method, HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(body)));
        return httpClient.send(builder.build(), HttpResponse.BodyHandlers.ofString());
    }
}
