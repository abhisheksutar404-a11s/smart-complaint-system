package com.example.smartcomplaintbackend.controller;

import java.util.List;

import com.example.smartcomplaintbackend.service.SparkAnalyticsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import java.util.Map;

import com.example.smartcomplaintbackend.model.Complaint;
import com.example.smartcomplaintbackend.service.ComplaintService;

@CrossOrigin(origins = "http://127.0.0.1:5500")
@RestController
@RequestMapping("/api/complaints")
public class ComplaintController {

    private final ComplaintService complaintService;
    private final SparkAnalyticsService sparkAnalyticsService;

    public ComplaintController(
            ComplaintService complaintService,
            SparkAnalyticsService sparkAnalyticsService) {

        this.complaintService = complaintService;
        this.sparkAnalyticsService = sparkAnalyticsService;
    }

    @GetMapping
    public List<Complaint> getAllComplaints() {
        return complaintService.getAllComplaints();
    }

    @PostMapping
    public Complaint createComplaint(@RequestBody Complaint complaint) {
        return complaintService.saveComplaint(complaint);
    }
    
    @PatchMapping("/{id}/status")
    public Complaint updateComplaintStatus(
            @PathVariable Long id,
            @RequestBody Map<String, String> request) {

        String status = request.get("status");

        return complaintService.updateComplaintStatus(id, status);
    }

    // Get dashboard statistics
    @GetMapping("/statistics")
    public Map<String, Long> getDashboardStatistics() {
        return complaintService.getDashboardStatistics();
    }

    // Get category statistics
    @GetMapping("/analytics/categories")
    public Map<String, Long> getCategoryStatistics() {
        return complaintService.getCategoryStatistics();
    }

    // Get priority statistics
    @GetMapping("/analytics/priorities")
    public Map<String, Long> getPriorityStatistics() {
        return complaintService.getPriorityStatistics();
    }

    // Get date statistics
    @GetMapping("/analytics/dates")
    public Map<String, Long> getDateStatistics() {
        return complaintService.getDateStatistics();
    }

    // Get status statistics
    @GetMapping("/analytics/statuses")
    public Map<String, Long> getStatusStatistics() {
        return complaintService.getStatusStatistics();
    }

    // Get Apache Spark category analytics
    @GetMapping("/spark/category-analytics")
    public Map<String, Long> getSparkCategoryAnalytics() {

        return sparkAnalyticsService.getCategoryAnalytics();
    }
}