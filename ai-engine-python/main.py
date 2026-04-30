import os
import json
import traceback
from typing import Optional
import fitz
import re
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from pydantic import BaseModel
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import write_log, clean_and_split_paper, format_references

# 导入我们刚刚拆分的三个模块
from config import QWEN_API_KEY, BASE_URL, INDEX_FILE, WIKI_DIR, RAW_DIR
from utils import write_log, clean_and_split_paper
from database import add_documents_to_db, delete_documents_by_source, collection

app = FastAPI(title="LLM Wiki Agentic Engine - Async & Modular Edition")

client = OpenAI(api_key=QWEN_API_KEY, base_url=BASE_URL)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


# ================== 1. 异步后台任务机制 ==================
def background_ingest_task(filename: str, raw_text: str, options: str):
    """后台任务：清理旧数据、结构化提取元数据、翻译摘要及选定特征"""
    try:
        write_log("ASYNC_START", f"开始高精度处理文献: {filename}")

        # 🌟 核心升级：覆盖模式下的“大扫除”
        md_filename = filename.replace(".pdf", ".md")
        delete_documents_by_source(filename)  # 1. 清理向量库中的旧块

        # 2. 清理 Index 目录中的旧记录
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                for line in lines:
                    if md_filename not in line:  # 如果不是这篇文献的记录，就写回
                        f.write(line)

        # ====== 下面是原有的处理逻辑 ======
        main_body, references_text = clean_and_split_paper(raw_text)

        chunks = text_splitter.split_text(main_body)
        add_documents_to_db(chunks, filename)

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
        write_log("LLM_INGEST", "正在请求 LLM 进行特征提取...")
        response = client.chat.completions.create(
            model="qwen3.6-plus",
            messages=[{"role": "user", "content": structured_prompt}]
        )
        final_markdown = response.choices[0].message.content

        final_markdown = re.sub(r'##\s*(📚\s*)?(参考文献|References).*', '', final_markdown,
                                flags=re.IGNORECASE | re.DOTALL).strip()
        if references_text:
            cleaned_refs = format_references(references_text)
            final_markdown += "\n\n## 📚 参考文献 (References)\n\n" + cleaned_refs

        with open(os.path.join(WIKI_DIR, md_filename), "w", encoding="utf-8") as f:
            f.write(final_markdown)

        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(f"- [{md_filename}](./{md_filename}) | 文献已完成深度解析\n")

        write_log("ASYNC_SUCCESS", f"✅ {filename} 结构化词条已生成")

    except Exception as e:
        import traceback
        traceback.print_exc()
        write_log("ASYNC_ERROR", f"❌ 任务失败: {str(e)}")

# 🌟文件查重接口
@app.get("/api/ai/check")
async def check_file_exists(filename: str):
    md_filename = filename.replace(".pdf", ".md")
    filepath = os.path.join(WIKI_DIR, md_filename)
    return {"exists": os.path.exists(filepath)}


# ================== 2. API 路由 ==================

# 接口 1：文档上传 (改造为瞬间返回的异步接口)
@app.post("/api/ai/process")
async def process_pdf(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        options: Optional[str] = Form("全文总结")
):
    try:
        write_log("UPLOAD", f"接收到文件上传请求: {file.filename}")

        # 1. 快速读取文件到内存（非常快，不会导致超时阻塞）
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        raw_pdf_text = "".join([page.get_text() for page in doc])

        # 备存原始文件到 Raw_Sources 文件夹
        raw_filepath = os.path.join(RAW_DIR, file.filename)
        with open(raw_filepath, "wb") as f:
            f.write(pdf_bytes)

        # 2. 🌟 核心魔法：将耗时十几秒到几分钟的处理任务扔进后台队列
        background_tasks.add_task(background_ingest_task, file.filename, raw_pdf_text, options)

        # 3. 立即响应前端
        return {
            "status": "success",
            "markdown": f"⏳ **任务已受理并丢入后台队列！**\n\n您的文献 `{file.filename}` 正在后台静默进行【智能切分】与【向量入库】。\n\n此时您可以无缝切换去右侧聊天框提问，后台完成后会自动更新至 Wiki 图谱！"
        }

    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": f"文件接收失败: {str(e)}"}


# ----------------- Agentic RAG 对话模块 -----------------

class ChatRequest(BaseModel):
    question: str


class SaveWikiRequest(BaseModel):
    topic: str
    content: str


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_wiki_index",
            "description": "读取本地 Wiki 库的总目录，了解目前拥有哪些文献和摘要信息。",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_wiki_page",
            "description": "读取某一篇具体的 Wiki markdown 页面内容。",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string", "description": "要读取的 .md 文件名（从 index 中获取）"}},
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_vector_db",
            "description": "在底层的海量原始论文向量数据库中进行深度检索。",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "用于检索的精炼关键词"}},
                "required": ["query"]
            }
        }
    }
]


# 接口 2：多路由智能问答
@app.post("/api/ai/chat")
async def agent_chat(request: ChatRequest):
    try:
        write_log("QUERY", f"用户提问: {request.question}")

        system_prompt = """
        你是一个拥有‘图书管理员’意识的高级科研管家。
        收到问题后，你的工作流程必须是：
        1. 优先调用 read_wiki_index 查看目录结构。
        2. 如果目录里有相关的页面，调用 read_wiki_page 读取具体内容。
        3. 如果 Wiki 中没有现成答案，调用 search_vector_db 在底层数据库检索。
        回答的最后，必须标明来源：[Wiki库] 或 [底层向量库]。
        """

        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": request.question}]

        for _ in range(3):
            response = client.chat.completions.create(model="qwen3.6-plus", messages=messages, tools=tools)
            msg = response.choices[0].message

            # Pydantic 兼容性安全补丁
            msg_dict = msg.model_dump(exclude_none=True)
            if "content" not in msg_dict or msg_dict["content"] is None:
                msg_dict["content"] = ""
            messages.append(msg_dict)

            if not msg.tool_calls:
                write_log("ANSWER", "思考完成，直接返回结果。")
                return {"answer": msg.content or "我查到了资料，但不知道怎么表达..."}

            tool_call = msg.tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            write_log("TOOL_CALL", f"大模型决定调用工具: {tool_name}, 参数: {args}")
            tool_result = ""

            try:
                if tool_name == "read_wiki_index":
                    with open(INDEX_FILE, "r", encoding="utf-8") as f:
                        tool_result = f.read()

                elif tool_name == "read_wiki_page":
                    filename = args.get("filename", "")
                    filepath = os.path.join(WIKI_DIR, filename)
                    if filename and os.path.exists(filepath):
                        with open(filepath, "r", encoding="utf-8") as f:
                            tool_result = f.read()
                    else:
                        tool_result = "该页面不存在。"

                elif tool_name == "search_vector_db":
                    query = args.get("query", "")
                    res = collection.query(query_texts=[query], n_results=3)
                    if res and "documents" in res and res["documents"] and res["documents"][0]:
                        tool_result = "\n---\n".join(res["documents"][0])
                    else:
                        tool_result = "未检索到相关内容。"
            except Exception as e:
                tool_result = f"工具执行报错: {str(e)}"
                write_log("TOOL_ERROR", f"执行 {tool_name} 失败: {str(e)}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": str(tool_result)
            })

        return {"answer": "思考超时或进入死循环，请简化您的问题。"}

    except Exception as e:
        traceback.print_exc()
        write_log("CHAT_ERROR", f"聊天接口发生严重异常: {str(e)}")
        return {"answer": f"❌ Python 引擎内部错误: {str(e)}"}


# 接口 3：知识库反哺
@app.post("/api/ai/save_to_wiki")
async def save_to_wiki(request: SaveWikiRequest):
    try:
        filename = f"新发现_{request.topic}.md"
        filepath = os.path.join(WIKI_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {request.topic}\n\n{request.content}\n")

        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(f"- [{filename}](./{filename}) | **来源**: 用户反哺 | **主题**: {request.topic}\n")

        write_log("FEEDBACK", f"用户将新知识反哺至 Wiki: {filename}")
        return {"status": "success", "message": f"成功保存至 Wiki 词条：{filename}"}
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

# 接口 4：获取已处理文献目录
@app.get("/api/ai/wiki/list")
async def get_wiki_list():
    try:
        # 读取 Wiki 文件夹下所有的 .md 文件 (排除 index 和 log)
        files = [f for f in os.listdir(WIKI_DIR) if f.endswith('.md') and not f.startswith(('index', 'log', '新发现'))]
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 接口 5：读取具体文献的 Wiki 内容
@app.get("/api/ai/wiki/content")
async def get_wiki_content(filename: str):
    try:
        filepath = os.path.join(WIKI_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return {"status": "success", "content": f.read()}
        return {"status": "error", "message": "文件不存在"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)