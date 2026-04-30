package com.wiki.llm_wiki.controller; // ⚠️ 请确保这里的包名和你原来的一致

import com.wiki.llm_wiki.service.WikiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity; // 🌟 修复: 引入 ResponseEntity
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate; // 🌟 修复: 引入 RestTemplate
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/wiki")
@CrossOrigin(origins = "*")
public class WikiController {

    @Autowired
    private WikiService wikiService;

    // 🌟 修复: 声明并实例化 RestTemplate 对象，供下面的接口使用
    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/upload")
    public String uploadPdf(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "options", required = false) List<String> options) {
        try {
            return wikiService.processUploadedPdf(file, options);
        } catch (Exception e) {
            return "❌ 处理失败: " + e.getMessage();
        }
    }

    @PostMapping("/chat")
    public String chat(@RequestBody Map<String, String> request) {
        String question = request.get("question");
        if (question == null || question.trim().isEmpty()) {
            return "问题不能为空哦！";
        }
        return wikiService.chatWithAgent(question);
    }

    @PostMapping("/save")
    public String saveToWiki(@RequestBody Map<String, String> request) {
        String topic = request.get("topic");
        String content = request.get("content");
        if (topic == null || content == null) {
            return "❌ 标题和内容不能为空";
        }
        return wikiService.saveToWiki(topic, content);
    }

    // ==========================================
    // 下面是获取图谱目录和内容的接口
    // ==========================================
    // 🌟 检查文献是否已存在
    @GetMapping("/check")
    public ResponseEntity<String> checkFile(@RequestParam("filename") String filename) {
        try {
            String url = "http://127.0.0.1:8000/api/ai/check?filename=" + filename;
            return restTemplate.getForEntity(url, String.class);
        } catch (Exception e) {
            return ResponseEntity.status(500).body("{\"status\":\"error\",\"message\":\"无法连接Python引擎\"}");
        }
    }

    @GetMapping("/list")
    public ResponseEntity<String> getWikiList() {
        System.out.println("🔍 [Java] 正在请求 Python 获取 Wiki 列表...");
        try {
            String url = "http://127.0.0.1:8000/api/ai/wiki/list";
            // 现在 restTemplate 和 ResponseEntity 都可以正常识别了
            return restTemplate.getForEntity(url, String.class);
        } catch (Exception e) {
            System.err.println("❌ [Java] 连接 Python 失败: " + e.getMessage());
            // 返回一个友好的 JSON 错误，防止前端直接弹 500
            return ResponseEntity.status(500).body("{\"status\":\"error\",\"message\":\"Python连接失败\"}");
        }
    }

    @GetMapping("/content")
    public ResponseEntity<String> getWikiContent(@RequestParam("filename") String filename) {
        System.out.println("📖 [Java] 正在请求 Python 读取内容: " + filename);
        try {
            String url = "http://127.0.0.1:8000/api/ai/wiki/content?filename=" + filename;
            return restTemplate.getForEntity(url, String.class);
        } catch (Exception e) {
            return ResponseEntity.status(500).body("{\"status\":\"error\",\"message\":\"无法读取文献内容\"}");
        }
    }
}