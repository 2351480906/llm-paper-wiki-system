import os
import json
import re
import shutil
import traceback
import pdfplumber
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# 导入你自己的配置文件和工具函数
from config import WIKI_DIR, INDEX_FILE, PDF_LIBRARY_DIR, CATALOG_FILE, QWEN_API_KEY, LLM_MODEL_NAME, BASE_URL
from utils import write_log, clean_and_split_paper, format_references

# ==========================================
# 🚀 1. 系统初始化与跨域配置
# ==========================================
app = FastAPI(title="Cyber Scholar AI Engine", version="2.0.0")

# 允许 Java/Vue 跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化阿里云通义千问客户端
client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url=BASE_URL
)


# ==========================================
# 📚 2. 核心辅助函数：账本管理
# ==========================================
def load_catalog() -> dict:
    """读取本地 PDF 智能图书馆的分类账本"""
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_to_catalog(filename: str, category: str, summary: str, file_path: str):
    """更新账本：记录新 PDF 的位置与摘要"""
    catalog = load_catalog()
    catalog[filename] = {
        "category": category,
        "summary": summary,
        "path": file_path
    }
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)


# ==========================================
# ⚙️ 3. 后台异步任务：智能路由与结构化提炼
# ==========================================
def background_ingest_task(filename: str, raw_text: str, options: str, temp_pdf_path: str):
    """
    大模型脏活累活后台管家：
    1. 给论文分类并移动实体文件。
    2. 提炼元数据、翻译摘要、提取特征公式。
    3. 登记造册写入 Wiki。
    """
    try:
        write_log("ASYNC_START", f"开始高精度处理并智能路由: {filename}")

        # 1. 文本预清洗（分离正文与参考文献）
        main_body, references_text = clean_and_split_paper(raw_text)

        # 2. 🌟 智能路由：让 LLM 判断分类
        category_prompt = f"请根据以下论文前言，给出一个精准的中文分类标签（字数在2-6个字之间，例如：计算机视觉、脑机接口、大语言模型）。只输出分类名称，不要标点：\n{main_body[:1500]}"
        cat_res = client.chat.completions.create(model=LLM_MODEL_NAME,
                                                 messages=[{"role": "user", "content": category_prompt}])
        category = cat_res.choices[0].message.content.strip().replace(" ", "_")

        # 3. 📂 物理归档：将临时 PDF 移动到对应的分类文件夹下
        category_dir = os.path.join(PDF_LIBRARY_DIR, category)
        os.makedirs(category_dir, exist_ok=True)
        final_pdf_path = os.path.join(category_dir, filename)

        # 如果文件已存在，先删除旧文件再移动（实现覆盖逻辑）
        if os.path.exists(final_pdf_path):
            os.remove(final_pdf_path)
        shutil.move(temp_pdf_path, final_pdf_path)

        # 4. 📝 结构化解析：提取元数据与公式特征
        structured_prompt = f"""
你是一个专业的科研论文解析助理。请仔细阅读提供的论文内容，并严格按照以下 Markdown 格式输出。

## 📋 元数据 (Metadata)
- **文献题目**：
- **文献作者**：
- **发表时间**：
- **发表地址/期刊会议**：
- **开源代码地址**：(若无请写“未提及”)

## 📖 论文摘要 (Abstract 中文翻译)
[注意：请不要自己总结，请直接找到原文中的 Abstract 章节，并将其完整、准确地翻译成中文。]

## 🔍 特征提取项
根据用户需求，请详细提取以下内容：{options}
(请针对每一项使用 '###' 子标题进行详细说明。如果涉及复杂数学公式请使用 LaTeX，但对于简单的数字和百分比（如 99.3%），请直接输出纯文本，绝对不要使用 $ 包裹！)

---
正文内容（前6000字）：
{main_body[:6000]}
"""
        write_log("LLM_INGEST", f"正在请求 LLM 解析文献特征...")
        response = client.chat.completions.create(
            model="LLM_MODEL_NAME",
            messages=[{"role": "user", "content": structured_prompt}]
        )
        final_markdown = response.choices[0].message.content

        # 5. 清理冗余并追加格式化好的参考文献
        final_markdown = re.sub(r'##\s*(📚\s*)?(参考文献|References).*', '', final_markdown,
                                flags=re.IGNORECASE | re.DOTALL).strip()
        if references_text:
            cleaned_refs = format_references(references_text)
            final_markdown += "\n\n## 📚 参考文献 (References)\n\n" + cleaned_refs

        # 6. 生成极简摘要，并记录到总账本
        summary_prompt = f"请用一句话总结这段文本的主旨：\n{final_markdown[:1000]}"
        summary = client.chat.completions.create(model=LLM_MODEL_NAME,
                                                 messages=[{"role": "user", "content": summary_prompt}]).choices[
            0].message.content.strip()

        # 更新 JSON 账本
        save_to_catalog(filename, category, summary, final_pdf_path)

        # 7. 保存到前端可见的 Wiki 图谱目录
        md_filename = filename.replace(".pdf", ".md")
        with open(os.path.join(WIKI_DIR, md_filename), "w", encoding="utf-8") as f:
            f.write(final_markdown)

        # 8. 更新 index.md 总索引
        # (先清除可能存在的旧记录，再追加新记录)
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                for line in lines:
                    if md_filename not in line:
                        f.write(line)

        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(f"- [{md_filename}](./{md_filename}) | 分类: {category} | 摘要: {summary}\n")

        write_log("ASYNC_SUCCESS", f"✅ {filename} 已归档至 [{category}] 文件夹，并生成 Wiki")

    except Exception as e:
        traceback.print_exc()
        write_log("ASYNC_ERROR", f"❌ 任务失败: {str(e)}")


# ==========================================
# 🌐 4. API 路由接口
# ==========================================

@app.get("/api/ai/check")
async def check_file_exists(filename: str):
    """前端防呆检测：检查文献是否已在知识库中"""
    md_filename = filename.replace(".pdf", ".md")
    filepath = os.path.join(WIKI_DIR, md_filename)
    return {"exists": os.path.exists(filepath)}


@app.post("/api/ai/wiki/upload")
async def upload_document(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        options: List[str] = Form(default=[])
):
    """接收文献，保存到临时目录，并转交后台处理"""
    try:
        # 1. 保存为临时物理文件
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_pdf_path = os.path.join(temp_dir, file.filename)

        with open(temp_pdf_path, "wb") as f:
            f.write(await file.read())

        # 2. 提取文本内容供清洗使用
        raw_text = ""
        with pdfplumber.open(temp_pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    raw_text += extracted + "\n"

        # 3. 推送至后台管家
        options_str = ", ".join(options)
        background_tasks.add_task(background_ingest_task, file.filename, raw_text, options_str, temp_pdf_path)

        return {"status": "success", "message": "文献已接收，后台正在进行智能分类与特征提取..."}
    except Exception as e:
        return {"status": "error", "message": f"处理失败: {str(e)}"}


class ChatRequest(BaseModel):
    question: str


@app.post("/api/ai/wiki/chat")
async def chat_with_agent(req: ChatRequest):
    """🌟 两阶段 Agentic RAG：先查账本目录，再读底层 PDF"""
    question = req.question
    catalog = load_catalog()

    try:
        # 🌟 阶段 1：全局目录感知
        catalog_str = json.dumps(catalog, ensure_ascii=False, indent=2)
        stage1_prompt = f"""
        用户提出了一个问题：“{question}”
        以下是我管理的所有物理 PDF 仓库目录和摘要信息：
        {catalog_str}

        请判断：
        1. 如果你可以通过一般常识直接回答，请直接回答。
        2. 如果必须查阅上述某篇特定文献才能详细解答，请回复严格格式：“NEED_PDF: [文件名.pdf]”，不要加任何其他废话。
        """
        res1 = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[{"role": "user", "content": stage1_prompt}]
        ).choices[0].message.content.strip()

        # 🌟 阶段 2：动态回溯底层 PDF 长上下文
        if "NEED_PDF:" in res1:
            target_file = res1.split("NEED_PDF:")[1].strip()

            # 在账本中寻找对应的实体文件
            matched_file = None
            for fn in catalog.keys():
                if fn in target_file:
                    matched_file = fn
                    break

            if matched_file:
                pdf_path = catalog[matched_file]["path"]
                write_log("AGENT_RAG", f"触发深度阅读，正在翻阅物理 PDF: {pdf_path}")

                # 读取原文件前 5 页进行精读
                pdf_content = ""
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        for i in range(min(5, len(pdf.pages))):
                            text = pdf.pages[i].extract_text()
                            if text: pdf_content += text + "\n"
                except Exception as e:
                    pdf_content = f"无法读取PDF内容: {str(e)}"

                stage2_prompt = f"""
                用户的问题是：“{question}”。
                你正在阅读原始论文 {matched_file} 的前几页内容：
                {pdf_content}

                请结合这些原文内容，给出详尽、专业的解答。
                ⚠️ 在回答的最后新起一行，必须加上这个标记：[底层原始PDF]
                """
                final_answer = client.chat.completions.create(
                    model=LLM_MODEL_NAME,
                    messages=[{"role": "user", "content": stage2_prompt}]
                ).choices[0].message.content
                return final_answer
            else:
                return "抱歉，我翻找了本地的物理仓库目录，但没有找到确切对应的 PDF 文件来回答这个问题。"
        else:
            # 常识或无需查阅文件即可回答
            return res1

    except Exception as e:
        return f"❌ 智能体运行出错: {str(e)}"


@app.get("/api/ai/wiki/list")
async def get_wiki_list():
    """获取所有已生成的 Wiki 列表"""
    try:
        if not os.path.exists(WIKI_DIR):
            return {"status": "success", "files": []}
        files = [f for f in os.listdir(WIKI_DIR) if f.endswith(".md") and f != "index.md"]
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/ai/wiki/content")
async def get_wiki_content(filename: str):
    """读取指定 Wiki 文献的内容"""
    try:
        filepath = os.path.join(WIKI_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return {"status": "success", "content": f.read()}
        return {"status": "error", "message": "知识库图谱中暂无此文件"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


class SaveWikiRequest(BaseModel):
    topic: str
    content: str


@app.post("/api/ai/wiki/save")
async def save_to_wiki(req: SaveWikiRequest):
    """将智能问答生成的优质内容手动固化为 Wiki"""
    try:
        # 清除特殊标记
        clean_content = req.content.replace("[底层原始PDF]", "").strip()
        filename = f"{req.topic}.md"
        filepath = os.path.join(WIKI_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"## 📖 AI 智能问答沉淀\n\n{clean_content}")

        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(f"- [{filename}](./{filename}) | 📌 由 Agent 智能问答动态生成沉淀\n")

        return {"status": "success", "message": "🎉 已成功沉淀至知识库图谱！"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 启动命令 (用于本地测试调试)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)