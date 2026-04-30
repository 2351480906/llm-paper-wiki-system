# 🧠 Cyber Scholar RAG - 智能学术文献图谱引擎

基于大语言模型 (LLM) 与 Agentic RAG 架构的沉浸式文献阅读与管理系统。

## ✨ 核心特性
- **🤖 三级路由 Agent**：自动判断查阅目录、精读文档或底层向量检索。
- **📑 结构化特征提取**：自动提炼论文元数据、摘要、算法结构及创新点，支持多选项组合。
- **⚡ 异步无阻塞架构**：后台静默向量化与 LLM 解析，前端秒级响应。
- **🧮 数学公式极速渲染**：完美解决 Markdown 语法冲突，原生支持 LaTeX 行内与块级渲染。
- **🌓 极客 UI 体验**：一键切换黑白双色主题，文献按层级精美卡片化展现。

## 🛠️ 技术栈
- **前端**：Vue 3 + Element Plus + Marked.js + KaTeX
- **中转后端**：Java 17 + Spring Boot
- **AI 引擎**：Python 3.10 + FastAPI + ChromaDB + LangChain + DashScope (Qwen)

## 🚀 快速启动

### 1. 启动 AI 引擎 (Python)
\`\`\`bash
cd ai-engine-python
pip install -r requirements.txt
# 请先在 config.py 中填入你的 QWEN_API_KEY
python main.py
\`\`\`

### 2. 启动中转层 (Java)
\`\`\`bash
cd backend-java
mvn spring-boot:run
\`\`\`

### 3. 启动前端控制台 (Vue)
\`\`\`bash
cd frontend-vue
npm install
npm run dev
\`\`\`