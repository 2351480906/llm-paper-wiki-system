```

### 3. 配置大模型
在后端的 `config.py` 中配置你的大模型 API 密钥（默认支持阿里云通义千问 `qwen-max` 及 `qwen-vl-plus`，也可无缝切换为 OpenAI GPT-4o 等支持 Function Calling 和 Vision 的模型）。

---

## 💡 使用工作流示例

1. **入库解析**：前端上传一篇学术 PDF（如 `EF-Net.pdf`）。
2. **后台流水线**：
   - 文本清洗 -> LLM 提取元数据、翻译摘要。
   - VLM 扫描全文档，剔除无用图标，提取架构图并生成上下文解析。
   - 最终生成包含图文的 `EF-Net.md` 并入库。
3. **多轮问答**：询问 Agent "EF-Net 到底用了什么模型结构？"，Agent 自主查目录 -> 读全文 -> 给出带公式的详细解答。
4. **知识融合**：点击回答下方的“沉淀至 Wiki”，AI 主编接手，将新知识无缝重写进 `EF-Net.md` 中。

---

## 🤝 贡献与许可
本项目为个人学习与探索大模型 Agent 架构的开源项目。欢迎提交 Issue 和 Pull Request 一这里是为你量身定制的 `README.md` 内容。它充分总结了我们一路走来开发的核心高级特性（多工具 Agent、多模态视觉解析、知识库智能反哺融合、现代化 UI 等），非常适合直接展示在你的 GitHub 主页上，彰显项目的技术深度！

请直接复制以下代码块中的所有 Markdown 内容：
```markdown
# 🧠 Cyber Scholar - 智能学术文献知识库 (Agentic & Multimodal RAG)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Vue](https://img.shields.io/badge/vue-3.0-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal)

## 📖 项目简介

**Cyber Scholar** 是一个高度现代化的 AI 学术助手与个人本地知识库系统。它突破了传统 RAG（检索增强生成）“查一次就回答”的死板模式，引入了先进的 **Agent 多步推理循环**、**多模态视觉大模型（VLM）图表解析**，以及创新的 **知识智能反哺融合（Smart Wiki Merge）** 机制。

每一次与文献的对话，都能精准转化为不断生长的专属知识树！

---

## ✨ 核心特性 (Core Features)

### 🤖 1. 自主推理智能体 (Agentic RAG)
- **多工具协作**：内置 `search_local_catalog`（查阅目录）和 `read_wiki_content`（深度阅读全文）等工具。
- **ReAct 循环**：Agent 拥有独立思考的 `while` 循环能力。遇到复杂问题，会自动先检索目录、再阅读正文，直到搜集齐所有证据才会向用户输出精美排版的最终答案。

### 👁️ 2. 多模态视觉解析 (Multimodal RAG)
- **精准提取**：底层使用 `PyMuPDF` 无损提取 PDF 原文插图。
- **AI 质检与精炼**：结合图片所在页的文字上下文，调用视觉大模型（如 `qwen-vl-plus`）进行联合研判。自动过滤无用的 Logo 和排版线条，精准总结核心 Figure 的结论，并图文并茂地追加至 Markdown 笔记中。

### 💾 3. 活体知识库反哺 (Smart Wiki Merge)
- **一键沉淀**：在精美的聊天界面中，遇到优质回答可一键点击“沉淀至 Wiki”。
- **语义排重**：后台特设“AI 主编”逻辑，大模型会智能寻找旧笔记中的相似概念（如识别“模型结构”与“算法架构”为同义词），将新细节补充进旧章节，彻底告别传统追加模式带来的数据冗余。

### 🎨 4. 现代高颜值交互体验
- 前端采用 Vue 3 + Element Plus 构建。
- 媲美主流 AI 助手的丝滑聊天体验：气泡式对话、完善的 Markdown 渲染（包含代码高亮、表格、数学公式）、思考加载动画以及动态图床展示。

---

## 🏗️ 系统架构与目录说明

后端 Python 服务采用了清晰的职责分离（Separation of Concerns）架构：

```text
📁 llm-paper-wiki-system/
├── 📄 config.py           # 全局配置 (路径、API Keys)
├── 📄 utils.py            # 通用工具函数 (PDF 拆分、文献清洗)
├── 📄 models.py           # Pydantic 数据模型层 (API 请求体定义)
├── 📄 ai_client.py        # 大模型引擎层 (全局 LLM 客户端初始化)
├── 📄 agent_tools.py      # Agent 智能体工具箱及说明书 (Tool Schema)
├── 📄 document_core.py    # 硬核流水线 (分类、特征提取、VLM 视觉解析、账本管理)
└── 📄 main.py             # FastAPI 入口 (仅保留清晰的路由分发)
```

*(注：系统支持通过 Java Spring Boot 作为 API Gateway 进行请求转发)*

---

## 🚀 快速开始

### 环境依赖
- Python 3.8+
- Node.js 16+

### 1. 启动后端引擎 (Python / FastAPI)
```bash
# 安装核心依赖
pip install fastapi uvicorn openai pymupdf pdfplumber pydantic

# 进入 Python 后端目录，启动服务 (默认端口 8000)
python main.py
```

### 2. 启动前端界面 (Vue 3)
```bash
# 进入前端目录
npm install

# 启动开发服务器
npm run dev
```

### 3. 配置大模型
在后端的 `config.py` 中配置你的大模型 API 密钥（默认支持阿里云通义千问 `qwen-max` 及 `qwen-vl-plus`，也可无缝切换为 OpenAI GPT-4o 等支持 Function Calling 和 Vision 的模型）。

---

## 💡 使用工作流示例

1. **入库解析**：前端上传一篇学术 PDF（如 `EF-Net.pdf`）。
2. **后台流水线**：
   - 文本清洗 -> LLM 提取元数据、翻译摘要。
   - VLM 扫描全文档，剔除无用图标，提取架构图并生成上下文解析。
   - 最终生成包含图文的 `EF-Net.md` 并入库。
3. **多轮问答**：询问 Agent "EF-Net 到底用了什么模型结构？"，Agent 自主查目录 -> 读全文 -> 给出带公式的详细解答。
4. **知识融合**：点击回答下方的“沉淀至 Wiki”，AI 主编接手，将新知识无缝重写进 `EF-Net.md` 中。

---

## 🤝 贡献与许可
本项目为个人学习与探索大模型 Agent 架构的开源项目。欢迎提交 Issue 和 Pull Request 一起优化！

License: [MIT](LICENSE)
```

```