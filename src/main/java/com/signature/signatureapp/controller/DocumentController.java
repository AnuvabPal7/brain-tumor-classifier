package com.signature.signatureapp.controller;

import com.signature.signatureapp.model.Document;
import com.signature.signatureapp.model.User;
import com.signature.signatureapp.service.DocumentService;
import com.signature.signatureapp.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/documents")
public class DocumentController {

    private final DocumentService documentService;
    private final UserService userService;

    public DocumentController(DocumentService documentService, UserService userService) {
        this.documentService = documentService;
        this.userService = userService;
    }

    @PostMapping("/upload")
    public ResponseEntity<?> uploadDocument(
            @RequestParam("file") MultipartFile file,
            @RequestParam("email") String email) { // For now, we manually pass user email to associate them
        try {
            Optional<User> userOpt = userService.findByEmail(email);
            if (userOpt.isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "User not found with provided email."));
            }

            Document savedDoc = documentService.storeDocument(file, userOpt.get());
            return ResponseEntity.ok(Map.of(
                    "message", "Document uploaded successfully!",
                    "documentId", savedDoc.getId(),
                    "fileName", savedDoc.getFileName()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}