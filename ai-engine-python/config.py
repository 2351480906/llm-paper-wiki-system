import os

QWEN_API_KEY = "your_api_key_here" # ⚠️ 替换为你的 Key
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 文件目录架构
BASE_DIR = "./my_knowledge_base"
WIKI_DIR = os.path.join(BASE_DIR, "Wiki")
RAW_DIR = os.path.join(BASE_DIR, "Raw_Sources")
SCHEMA_DIR = os.path.join(BASE_DIR, "Schema")

INDEX_FILE = os.path.join(WIKI_DIR, "index.md")
LOG_FILE = os.path.join(WIKI_DIR, "log.md")
SCHEMA_FILE = os.path.join(SCHEMA_DIR, "rule.yaml")

# 启动时自动初始化目录结构
for directory in [WIKI_DIR, RAW_DIR, SCHEMA_DIR]:
    os.makedirs(directory, exist_ok=True)

if not os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write("# 📚 本地知识库总目录 (Wiki Index)\n\n")

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("# ⏱️ 知识库操作审计日志\n\n")

if not os.path.exists(SCHEMA_FILE):
    with open(SCHEMA_FILE, 'w', encoding='utf-8') as f:
        f.write("wiki_rules:\n  - 所有新建页面必须包含一句话摘要。\n  - 专业术语请加粗。\n  - 必须标明知识来源。\n")