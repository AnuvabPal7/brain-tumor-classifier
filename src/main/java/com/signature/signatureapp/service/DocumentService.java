package com.signature.signatureapp.service;

import com.signature.signatureapp.model.Document;
import com.signature.signatureapp.model.User;
import com.signature.signatureapp.repository.DocumentRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class DocumentService {

    private final DocumentRepository documentRepository;
    
    // This is the local directory where your PDFs will live
    private final String uploadDir = "D:/signature-app/uploads/";

    public DocumentService(DocumentRepository documentRepository) {
        this.documentRepository = documentRepository;
        
        // This block auto-creates the upload folder on your computer if it doesn't exist
        File directory = new File(uploadDir);
        if (!directory.exists()) {
            directory.mkdirs();
        }
    }

    public Document storeDocument(MultipartFile file, User user) throws Exception {
        // 1. Double check that the file isn't empty
        if (file.isEmpty()) {
            throw new IllegalArgumentException("Failed to store empty file.");
        }

        // 2. Generate a unique name using UUID (e.g., 550e8400-e29b-file.pdf)
        String originalFileName = file.getOriginalFilename();
        String uniqueFileName = UUID.randomUUID().toString() + "_" + originalFileName;

        // 3. Save the physical file onto your local drive
        Path targetPath = Paths.get(uploadDir + uniqueFileName);
        Files.copy(file.getInputStream(), targetPath);

        // 4. Create a document record and link it to the uploading user
        Document document = new Document();
        document.setFileName(originalFileName);
        document.setFilePath(targetPath.toString());
        document.setFileType(file.getContentType());
        document.setUploadedAt(LocalDateTime.now());
        document.setUploader(user);

        // 5. Save the metadata info to your database
        return documentRepository.save(document);
    }
}