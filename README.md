# 🧠 Cyber Scholar: Agentic Multimodal RAG System

Cyber Scholar 是一个高度现代化的**多模态智能体文献知识库系统 (Agentic Multimodal RAG)**。
它不仅能对上传的学术 PDF 进行全自动的结构化解析，还引入了具备多步推理能力的 Agent（智能体）、VLM 视觉大模型辅助解析，以及独创的“知识库动态生长”机制，彻底颠覆传统的静态纯文本 RAG 体验。

## ✨ 核心硬核特性 (Core Features)

### 1. 🤖 基于 ReAct 的 Agentic RAG (多步推理与工具调用)
传统的 RAG 系统只能进行“单次检索-生成”。Cyber Scholar 搭载了原生 Agent 循环大脑：
- **自主思考与工具调度**：当面对复杂问题（如“某文献的具体损失函数公式是什么”），Agent 会自主决定先调用 `search_local_catalog` 查阅目录，若信息不足，会继续调用 `read_wiki_content` 深度阅读文献全文，直至拼凑出完整答案。
- **最多 5 轮深度推理**：突破单次对话限制，Agent 具备多轮观察与行动能力，极大提升长文本事实问答的准确率。

### 2. 👁️ 多模态视觉解析 (Multimodal Vision Engine)
不仅仅是纯文本！系统内置强大的 `PyMuPDF + VLM (如 Qwen-VL-Plus)` 视觉处理流水线：
- **上下文感知**：提取 PDF 图片时，同步提取当页的纯文本作为“上下文背景”发给视觉大模型。
- **智能质检与垃圾过滤**：视觉大模型兼职“质检员”，自动识别并丢弃 Logo、排版线条等无价值图片（拦截 `IGNORE` 信号），保证知识库图床纯净。
- **专业一句话图解**：为每一张保留下来的核心架构图、数据图表生成结合论文上下文的精炼解析，并自动插入 Markdown 笔记中。

### 3. 🌱 知识库动态生长与智能融合 (Dynamic Wiki Evolution)
告别看完就忘的聊天记录，让你的知识图谱越用越厚：
- **一键沉淀至 Wiki**：在现代化的高颜值聊天界面中，遇到 Agent 给出的优质回答，点击【沉淀至 Wiki】即可触发融合。
- **LLM 语义防重覆写**：后台 AI 主编会自动读取对应文献的旧笔记，进行“同义词查重”（如将新问的“模型结构”补充进旧的“算法架构”标题下），无缝将新知识揉进旧笔记，彻底消灭信息冗余。

### 4. 🎨 现代通讯级 UI 体验 (Modern Chat UI)
采用 Vue 3 + Element Plus 构建，彻底告别传统的学术冰冷感：
- 经典的左右分立式气泡聊天布局（User蓝底靠右，AI白底靠左）。
- 流畅的 Agent 思考（Typing）加载动画与 Markdown 实时渲染。
- 优雅的代码块高亮与响应式图片自适应展示。

---

## 🏗️ 架构与目录结构 (Architecture)

系统后端采用典型的“职责分离 (Separation of Concerns)”架构，基于 FastAPI 构建：
```text
📁 llm-paper-wiki-system/
├── 📄 config.py           # 全局配置 (路径、API Keys)
├── 📄 utils.py            # 通用工具函数 (PDF 拆分、文献格式化)
├── 📄 models.py           # Pydantic 数据模型层 (定义 API 请求体)
├── 📄 ai_client.py        # 大模型客户端初始化 (单例模式)
├── 📄 agent_tools.py      # Agent 工具箱 (查目录、深度阅读等能力)
├── 📄 document_core.py    # 核心引擎 (文献入库流水线、多模态视觉解析、账本读写)
└── 📄 main.py             # 极简入口 (仅包含 FastAPI 路由和跨域配置)

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
