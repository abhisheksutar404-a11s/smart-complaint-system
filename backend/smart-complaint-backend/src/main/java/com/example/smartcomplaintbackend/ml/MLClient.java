package com.example.smartcomplaintbackend.ml;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

@Component
public class MLClient {

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;

    private final String mlServiceUrl =
            "http://127.0.0.1:8000/predict";

    public MLClient() {
        this.httpClient = HttpClient.newHttpClient();
        this.objectMapper = new ObjectMapper();
    }

    public PredictionResult predict(String complaint) {

        try {

            // Create JSON request
            String requestBody = objectMapper.writeValueAsString(
                    Map.of("complaint", complaint)
            );

            // Create HTTP POST request
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(mlServiceUrl))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                    .build();

            // Send request to Python ML service
            HttpResponse<String> response = httpClient.send(
                    request,
                    HttpResponse.BodyHandlers.ofString()
            );

            // Check response
            if (response.statusCode() != 200) {

                throw new RuntimeException(
                        "ML service returned status: "
                                + response.statusCode()
                );
            }

            // Read JSON response
            JsonNode json =
                    objectMapper.readTree(response.body());

            String category =
                    json.get("category").asText();

            double confidence =
                    json.get("confidence").asDouble();

            // Return both values separately
            return new PredictionResult(category, confidence);

        } catch (Exception e) {

            throw new RuntimeException(
                    "Failed to communicate with ML service",
                    e
            );
        }
    }

    // Structure for ML prediction result
    public record PredictionResult(
            String category,
            double confidence
    ) {
    }
}