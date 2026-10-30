
package com.example.smartcomplaintbackend.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.example.smartcomplaintbackend.model.Complaint;

public interface ComplaintRepository extends JpaRepository<Complaint, Long> {

    // Count complaints by status
    long countByStatus(String status);

    // Count complaints grouped by category
    @Query("SELECT c.category, COUNT(c) FROM Complaint c GROUP BY c.category")
    List<Object[]> countComplaintsByCategory();
        
    // Count complaints grouped by priority
    @Query("SELECT c.priority, COUNT(c) FROM Complaint c GROUP BY c.priority")
    List<Object[]> countComplaintsByPriority();


    // Count complaints grouped by date
    @Query(value = """
            SELECT DATE(created_at), COUNT(*)
            FROM complaint
            WHERE created_at IS NOT NULL
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
            """, nativeQuery = true)
    List<Object[]> countComplaintsByDate();


    // Count complaints grouped by status
    @Query("SELECT c.status, COUNT(c) FROM Complaint c GROUP BY c.status")
    List<Object[]> countComplaintsByStatus();
}
