package com.rapidcare.api.controllers;
import com.rapidcare.api.services.ClassifyTextService;
import com.rapidcare.api.services.VoiceToTextService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;

@RestController
@RequestMapping("/api")
public class APIController {
    @Autowired
    private VoiceToTextService voiceToTextService;
    @Autowired
    private ClassifyTextService classifyTextService;

    @CrossOrigin(origins = "http://localhost:3000")
    @PostMapping("/classifyText")
    public ResponseEntity<String> classifyData(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("File is empty");
        }

        try {
            byte[] soundBytes = file.getBytes();

            String filePath = "C:\\Users\\prana\\Downloads\\test.wav"; // Specify your desired save path
            File savedFile = new File(filePath);
            file.transferTo(savedFile);

            String resp = voiceToTextService.hitVoicetoText(savedFile);
            System.out.println("------------" + resp);
            return ResponseEntity.status(HttpStatus.ACCEPTED).body("Classification process not yet implemented." + resp);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Backend error has occurred");
        }
    }

    @GetMapping("/heartbeat")
    public String isUp(){
        return "API is up and well";
    }
}
