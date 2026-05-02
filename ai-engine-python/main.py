import os
import json
import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 导入配置与我们的核心模块
from config import WIKI_DIR, INDEX_FILE, LLM_MODEL_NAME
from models import SettingsConfig, ChatRequest, MergeWikiRequest, SaveWikiRequest
from ai_client import client
from agent_tools import AGENT_TOOLS, search_local_catalog, read_wiki_content
from document_core import background_ingest_task, IMAGE_DIR

app = FastAPI(title="Cyber Scholar AI Engine", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载图床服务
app.mount("/api/wiki/images", StaticFiles(directory=IMAGE_DIR), name="images")

# ================= API 路由 =================

@app.post("/api/ai/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...), options: list[str] = Form(default=[])):
    try:
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_pdf_path = os.path.join(temp_dir, file.filename)

        with open(temp_pdf_path, "wb") as f: f.write(await file.read())

        raw_text = ""
        with pdfplumber.open(temp_pdf_path) as pdf:
            for page in pdf.pages:
                if extracted := page.extract_text(): raw_text += extracted + "\n"

        background_tasks.add_task(background_ingest_task, file.filename, raw_text, ", ".join(options), temp_pdf_path)
        return {"status": "success", "message": "文献已接收，后台正在进行处理..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/ai/chat")
async def chat_with_agent(req: ChatRequest):
    try:
        messages = [{"role": m.role, "content": m.content} for m in req.messages]
        messages.insert(0, {"role": "system", "content": "你是 Cyber Scholar。你必须善用工具来回答问题。"})

        max_loops, loop_count, final_answer = 5, 0, ""

        while loop_count < max_loops:
            loop_count += 1
            print(f"🧠 [Agent] 第 {loop_count} 轮思考中...")
            response = client.chat.completions.create(model=LLM_MODEL_NAME, messages=messages, tools=AGENT_TOOLS, tool_choice="auto")
            response_message = response.choices[0].message

            if response_message.tool_calls:
                assistant_msg = response_message.model_dump(exclude_none=True)
                if not assistant_msg.get("content"): assistant_msg["content"] = ""
                messages.append(assistant_msg)

                for tool_call in response_message.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    if tool_call.function.name == "search_local_catalog":
                        result = search_local_catalog(args.get("keyword", ""))
                    elif tool_call.function.name == "read_wiki_content":
                        result = read_wiki_content(args.get("filename", ""))
                    messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": tool_call.function.name, "content": result})
                continue
            else:
                final_answer = response_message.content
                break

        return {"status": "success", "content": final_answer or "✅ 尝试完毕，未提炼出有效文本。"}
    except Exception as e:
        return {"content": f"❌ 智能体运行出错: {str(e)}"}

@app.post("/api/ai/wiki/merge")
async def merge_to_wiki(req: MergeWikiRequest):
    try:
        filename = req.filename.replace('.pdf', '.md') if req.filename.endswith('.pdf') else (req.filename if req.filename.endswith('.md') else req.filename + '.md')
        file_path = os.path.join(WIKI_DIR, filename)
        if not os.path.exists(file_path): return {"status": "error", "message": "未找到原始 Wiki"}

        with open(file_path, 'r', encoding='utf-8') as f: existing_content = f.read()

        sys_prompt = "你是一个知识库主编。将新Q&A融合到旧笔记中。严禁重复标题，排重补充细节。直接输出完整Markdown。"
        user_prompt = f"【旧笔记】:\n{existing_content}\n\n【新Q&A】:\nQ: {req.question}\nA: {req.answer}\n\n输出最新Markdown："

        response = client.chat.completions.create(model=LLM_MODEL_NAME, messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}])
        new_content = response.choices[0].message.content.strip().strip("```markdown").strip("```").strip()

        with open(file_path, 'w', encoding='utf-8') as f: f.write(new_content)
        return {"status": "success", "content": "🎉 知识已完美融合！"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 基础的 List / Content / Save API 由于篇幅问题，直接平移进来即可
@app.get("/api/ai/list")
async def get_wiki_list():
    return {"status": "success", "files": [f for f in os.listdir(WIKI_DIR) if f.endswith(".md") and f != "index.md"]}

@app.get("/api/ai/content")
async def get_wiki_content(filename: str):
    with open(os.path.join(WIKI_DIR, filename), "r", encoding="utf-8") as f:
        return {"status": "success", "content": f.read()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)