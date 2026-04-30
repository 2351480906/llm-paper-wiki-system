plugins {
    java
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "com.wiki"
version = "0.0.1-SNAPSHOT"
description = "LLM_wiki"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-webmvc")
    testImplementation("org.springframework.boot:spring-boot-starter-webmvc-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
    // 1. PDFBox：用于读取本地 PDF 文件并提取纯文本
    implementation("org.apache.pdfbox:pdfbox:3.0.2")

    // 2. LangChain4j：用于调用 Qwen 大模型 (Qwen 兼容 OpenAI 的 API 格式)
    implementation("dev.langchain4j:langchain4j-open-ai:0.30.0")

    implementation("com.fasterxml.jackson.core:jackson-databind")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
