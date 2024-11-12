package com.rapidcare.api.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.io.File;

@Service
public class VoiceToTextService {
    @Value("${services.vtt}")
    private String vttServiceRoute;

    @Autowired
    private RestTemplate restTemplate;

    public String hitVoicetoText(File temp){
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", new FileSystemResource(temp));

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        ResponseEntity<String> response = restTemplate.exchange(
                "http://127.0.0.1:5000/voice_to_text",
                HttpMethod.POST,
                requestEntity,
                String.class
        );

        return response.getBody();
    }
}
