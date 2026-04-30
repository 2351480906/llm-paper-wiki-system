package com.wiki.llm_wiki; // 注意：这里要换成你自己的包名！

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Duration;

public class WikiEngineTest {

    // ================== 请在这里修改你的配置 ==================
    // 1. 你刚刚准备好的 PDF 文件路径
    private static final String PDF_FILE_PATH = "C:\\Users\\23514\\OneDrive\\Desktop\\文献\\STA-Net.pdf";

    // 2. 你的 通义千问 (Qwen) API KEY
    private static final String QWEN_API_KEY = "sk-21b28f745dee492ab5c8a4de46d9413b";

    // 3. 生成的 Markdown 文件想保存在哪里（比如保存到桌面）
    private static final String OUTPUT_MD_PATH = "D:\\test-output.md";
    // ==========================================================

    public static void main(String[] args) {
        System.out.println("🚀 任务开始！");

        try {
            // 第 1 步：读取 PDF 内容
            System.out.println("📄 正在读取 PDF 文件...");
            String pdfText = extractTextFromPdf(PDF_FILE_PATH);
            System.out.println("✅ PDF 读取成功，共提取 " + pdfText.length() + " 个字符。");

            // 由于测试阶段不想消耗太多 Token，我们只截取前 3000 个字符发给大模型
            String textToSend = pdfText.length() > 3000 ? pdfText.substring(0, 3000) : pdfText;

            // 第 2 步：初始化 Qwen 大模型 (使用兼容 OpenAI 的接口格式)
            System.out.println("🤖 正在连接 Qwen 大模型...");
            ChatLanguageModel model = OpenAiChatModel.builder()
                    // 这是阿里云百炼（通义千问）的兼容调用地址
                    .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                    .apiKey(QWEN_API_KEY)
                    .modelName("qwen3.6-plus") // 或者使用 qwen-turbo
                    .timeout(Duration.ofMinutes(2)) // 给大模型两分钟的思考时间
                    .build();

            // 第 3 步：设定 Prompt (提示词) 并调用大模型
            String prompt = """
                    你是一个专业的科研助手。请阅读以下论文的片段，并提取关键信息。
                    必须以标准的 Markdown 格式输出，包含以下内容：
                    # 论文标题
                    ## 作者
                    ## 研究背景与核心方法
                    ## 简要总结
                    
                    论文片段如下：
                    """ + textToSend;

            System.out.println("⏳ 正在让 LLM 进行总结，请耐心等待（可能需要十几秒）...");
            String resultMarkdown = model.generate(prompt);
            System.out.println("✅ LLM 总结完成！");

            // 第 4 步：将结果写入本地的 .md 文件
            Path outputPath = Paths.get(OUTPUT_MD_PATH);
            Files.writeString(outputPath, resultMarkdown);
            System.out.println("🎉 大功告成！Markdown 文件已保存至：" + OUTPUT_MD_PATH);

        } catch (Exception e) {
            System.err.println("❌ 运行出错：");
            e.printStackTrace();
        }
    }

    /**
     * 使用 PDFBox 提取 PDF 纯文本的辅助方法
     */
    private static String extractTextFromPdf(String filePath) throws IOException {
        File file = new File(filePath);
        if (!file.exists()) {
            throw new RuntimeException("找不到 PDF 文件：" + filePath);
        }
        // 注意：这里改成了 Loader.loadPDF(file)
        try (PDDocument document = org.apache.pdfbox.Loader.loadPDF(file)) {
            PDFTextStripper stripper = new PDFTextStripper();
            return stripper.getText(document);
        }
    }
}