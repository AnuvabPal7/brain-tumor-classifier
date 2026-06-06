package com.signature.signatureapp.repository;

import com.signature.signatureapp.model.Document;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface DocumentRepository extends JpaRepository<Document, Long> {
    // Find all documents uploaded by a specific user id
    List<Document> findByUploaderId(Long userId);
}