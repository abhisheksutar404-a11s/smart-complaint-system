
package com.example.smartcomplaintbackend.service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

import org.springframework.stereotype.Service;

import com.example.smartcomplaintbackend.model.Complaint;
import com.example.smartcomplaintbackend.repository.ComplaintRepository;
import com.example.smartcomplaintbackend.ml.MLClient;

@Service
public class ComplaintService {

    private final ComplaintRepository complaintRepository;
    private final MLClient mlClient;

    public ComplaintService(
            ComplaintRepository complaintRepository,
            MLClient mlClient) {

        this.complaintRepository = complaintRepository;
        this.mlClient = mlClient;
    }

    // Save a new complaint
    public Complaint saveComplaint(Complaint complaint) {

        try {
            // Send complaint description to ML service
            MLClient.PredictionResult result =
                    mlClient.predict(complaint.getDescription());

            // Store ML prediction in complaint
            complaint.setPredictedCategory(result.category());
            complaint.setConfidence(result.confidence());

            System.out.println("ML Prediction: Category: "
                    + result.category()
                    + ", Confidence: "
                    + result.confidence());

        } catch (RuntimeException e) {

            // ML service unavailable; save without prediction
            complaint.setPredictedCategory(null);
            complaint.setConfidence(null);

            System.err.println(
                    "AI prediction unavailable. Saving complaint without prediction."
            );

            System.err.println("Reason: " + e.getMessage());
        }

        // Generate creation timestamp automatically
        complaint.setCreatedAt(LocalDateTime.now());

        // Save complaint whether AI prediction succeeds or fails
        return complaintRepository.save(complaint);
        }

    // Get all complaints
    public List<Complaint> getAllComplaints() {

        return complaintRepository.findAll();
    }

    // Update complaint status
    public Complaint updateComplaintStatus(Long id, String status) {

        Complaint complaint = complaintRepository.findById(id)
                .orElseThrow(() -> new RuntimeException(
                        "Complaint not found with ID: " + id
                ));

        complaint.setStatus(status);

        return complaintRepository.save(complaint);
    }

    // Get dashboard statistics
    public Map<String, Long> getDashboardStatistics() {

        Map<String, Long> statistics = new LinkedHashMap<>();

        statistics.put(
                "totalComplaints",
                complaintRepository.count()
        );

        statistics.put(
                "open",
                complaintRepository.countByStatus("Pending")
        );

        statistics.put(
                "inProgress",
                complaintRepository.countByStatus("In Progress")
        );

        statistics.put(
                "resolved",
                complaintRepository.countByStatus("Resolved")
        );

        return statistics;
    }

    // Get complaints grouped by category
    public Map<String, Long> getCategoryStatistics() {

        Map<String, Long> categoryStatistics = new LinkedHashMap<>();

        List<Object[]> results =
                complaintRepository.countComplaintsByCategory();

        for (Object[] result : results) {

            String category = (String) result[0];
            Long count = (Long) result[1];

            categoryStatistics.put(category, count);
        }

        return categoryStatistics;
    }
    
    // Get complaints grouped by priority
        public Map<String, Long> getPriorityStatistics() {

        Map<String, Long> priorityStatistics = new LinkedHashMap<>();

        List<Object[]> results =
                complaintRepository.countComplaintsByPriority();

        for (Object[] result : results) {

                String priority = (String) result[0];
                Long count = (Long) result[1];

                priorityStatistics.put(priority, count);
        }

        return priorityStatistics;
        }

        // Get complaints grouped by date
        public Map<String, Long> getDateStatistics() {

        Map<String, Long> dateStatistics = new LinkedHashMap<>();

        List<Object[]> results =
                complaintRepository.countComplaintsByDate();

        for (Object[] result : results) {

                String date = result[0].toString();
                Long count = ((Number) result[1]).longValue();

                dateStatistics.put(date, count);
        }

        return dateStatistics;
        }

        // Get complaints grouped by status
        public Map<String, Long> getStatusStatistics() {

        Map<String, Long> statusStatistics = new LinkedHashMap<>();

        List<Object[]> results =
                complaintRepository.countComplaintsByStatus();

        for (Object[] result : results) {

                String status = (String) result[0];
                Long count = (Long) result[1];

                statusStatistics.put(status, count);
        }

        return statusStatistics;
        }
}
