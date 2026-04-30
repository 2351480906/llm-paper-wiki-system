package com.wiki.llm_wiki.service; // ⚠️ 换成你自己的包名

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class WikiService {

    @Value("${app.obsidian.vault-path}")
    private String vaultPath;

    @Value("${app.ai-engine.url}")
    private String aiEngineUrl;

    @Value("${app.ai-engine.chat-url}")
    private String aiChatUrl;

    @Value("${app.ai-engine.save-wiki-url}")
    private String aiSaveWikiUrl;

    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    // 1. 处理上传
    public String processUploadedPdf(MultipartFile file, List<String> options) throws IOException {
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() { return file.getOriginalFilename(); }
        });
        body.add("options", (options != null) ? String.join("、", options) : "全文总结");

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        ResponseEntity<String> response = restTemplate.postForEntity(aiEngineUrl, requestEntity, String.class);
        try {
            JsonNode root = objectMapper.readTree(response.getBody());
            if ("success".equals(root.get("status").asText())) {
                String markdownContent = root.get("markdown").asText();
                return saveToObsidian(file.getOriginalFilename(), markdownContent);
            } else {
                throw new RuntimeException(root.get("message").asText());
            }
        } catch (Exception e) {
            throw new RuntimeException("解析失败: " + e.getMessage());
        }
    }

    // 2. 处理聊天
    public String chatWithAgent(String question) {
        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("question", question);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(requestBody, headers);

        try {
            ResponseEntity<String> response = restTemplate.postForEntity(aiChatUrl, requestEntity, String.class);
            JsonNode root = objectMapper.readTree(response.getBody());
            return root.get("answer").asText();
        } catch (Exception e) {
            return "❌ 抱歉，大脑开小差了: " + e.getMessage();
        }
    }

    // 3. 🌟 新增：反哺 Wiki
    public String saveToWiki(String topic, String content) {
        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("topic", topic);
        requestBody.put("content", content);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(requestBody, headers);

        try {
            ResponseEntity<String> response = restTemplate.postForEntity(aiSaveWikiUrl, requestEntity, String.class);
            JsonNode root = objectMapper.readTree(response.getBody());
            if ("success".equals(root.get("status").asText())) {
                return "✅ " + root.get("message").asText();
            } else {
                return "❌ 保存失败: " + root.get("message").asText();
            }
        } catch (Exception e) {
            return "❌ 保存请求失败: " + e.getMessage();
        }
    }

    // 内部方法：存入本地 Obsidian
    private String saveToObsidian(String originalFilename, String content) throws IOException {
        Path vaultDir = Paths.get(vaultPath);
        if (!Files.exists(vaultDir)) Files.createDirectories(vaultDir);
        String fileName = originalFilename.replace(".pdf", "") + ".md";
        Path outputPath = vaultDir.resolve(fileName);
        Files.writeString(outputPath, content);
        return "✅ 处理成功！已同步至 Obsidian: " + fileName;
    }
}