
package com.example.smartcomplaintbackend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;

@Service
public class SparkAnalyticsService {

    @Value("${spark.analytics.file}")
    private String csvFilePath;

    public Map<String, Long> getCategoryAnalytics() {

        Map<String, Long> analytics = new LinkedHashMap<>();

        Path path = Path.of(csvFilePath);

        if (!Files.exists(path)) {
            throw new RuntimeException(
                "Spark analytics CSV file not found: " + csvFilePath
            );
        }

        try (BufferedReader reader = Files.newBufferedReader(path)) {

            // Skip the CSV header: category,count
            String line = reader.readLine();

            while ((line = reader.readLine()) != null) {

                if (line.isBlank()) {
                    continue;
                }

                String[] values = line.split(",", 2);

                if (values.length != 2) {
                    throw new RuntimeException(
                        "Invalid row in Spark analytics CSV: " + line
                    );
                }

                String category = values[0].trim();
                long count = Long.parseLong(values[1].trim());

                analytics.put(category, count);
            }

        } catch (IOException e) {
            throw new RuntimeException(
                "Unable to read Spark analytics CSV file", e
            );
        }

        return analytics;
    }
}
