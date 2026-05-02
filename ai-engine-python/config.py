import os
import json
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
QWEN_API_KEY = "your-api-key" # ⚠️ 记得填回你的 API Key
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 1. 设置默认配置
DEFAULT_CONFIG = {
    "base_path": os.path.join(BASE_DIR, "my_knowledge_base"),
    "llm_model": "qwen3.6-plus"
}

# 2. 从外部 JSON 加载用户自定义配置
if os.path.exists(SETTINGS_FILE):
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            user_config = json.load(f)
    except:
        user_config = DEFAULT_CONFIG
else:
    user_config = DEFAULT_CONFIG

# 3. 导出全局变量
KNOWLEDGE_BASE_DIR = user_config.get("base_path", DEFAULT_CONFIG["base_path"])
LLM_MODEL_NAME = user_config.get("llm_model", DEFAULT_CONFIG["llm_model"])

# 4. 动态生成下级目录
WIKI_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "Wiki")

# 🌟 核心架构升级：原始资源池 (Raw_Sources)
RAW_SOURCES_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "Raw_Sources")
PDF_LIBRARY_DIR = os.path.join(RAW_SOURCES_DIR, "PDF")
# 未来你如果加了 Word，只需在这里加一行 WORD_LIBRARY_DIR = os.path.join(RAW_SOURCES_DIR, "Word") 即可

CATALOG_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "pdf_catalog.json")
INDEX_FILE = os.path.join(WIKI_DIR, "index.md")
LOG_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "agent.log")

# ==========================================
# 🔄 自动迁移逻辑 (无损兼容老版本)
# ==========================================
OLD_PDF_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "Categorized_PDFs")
if os.path.exists(OLD_PDF_DIR) and not os.path.exists(PDF_LIBRARY_DIR):
    # 确保父级 Raw_Sources 文件夹存在
    os.makedirs(RAW_SOURCES_DIR, exist_ok=True)
    # 将原来的 Categorized_PDFs 整个移动并重命名为 PDF
    shutil.move(OLD_PDF_DIR, PDF_LIBRARY_DIR)
    print(f"📦 [系统管家] 检测到历史数据，已自动无损迁移至: {PDF_LIBRARY_DIR}")

# 5. 确保所有目录存在
os.makedirs(WIKI_DIR, exist_ok=True)
os.makedirs(RAW_SOURCES_DIR, exist_ok=True)
os.makedirs(PDF_LIBRARY_DIR, exist_ok=True)
