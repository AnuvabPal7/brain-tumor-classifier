package com.signature.signatureapp.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "documents")
@Data
public class Document {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fileName;
    private String filePath;
    private String fileType;
    private LocalDateTime uploadedAt;

    // This tracks which user uploaded the document
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User uploader;
}