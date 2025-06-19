package com.perfguard.perfguard;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
public class MockController {

    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestBody Map<String, String> body) throws InterruptedException {
        Thread.sleep(100); // simulate delay
        return ResponseEntity.ok("Logged in as " + body.getOrDefault("user", "unknown"));
    }

    @GetMapping("/search")
    public ResponseEntity<List<String>> search(@RequestParam String query) throws InterruptedException {
        Thread.sleep(150);
        return ResponseEntity.ok(List.of("Result 1 for " + query, "Result 2 for " + query));
    }
}
