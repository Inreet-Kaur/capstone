package com.rapidcare.api.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ClassifyTextService {
    @Value("${services.clft}")
    private String clftServiceRoute;

    @Autowired
    private RestTemplate restTemplate;

    public String [] classifyData(String [] sentences){
        String url = "http://localhost:5000/your-endpoint";

        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");

        HttpEntity<Object> request = new HttpEntity<>(sentences, headers);

        ResponseEntity<String> response = restTemplate.exchange(
                clftServiceRoute,
                HttpMethod.POST,
                request,
                String.class
        );

//        return response.getBody();
        return new String[]{"Classified Text"};
    }
}
