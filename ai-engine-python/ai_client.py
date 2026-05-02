from openai import OpenAI
from config import QWEN_API_KEY, BASE_URL

# 全局单例 LLM 客户端，其他文件都从这里 import client
client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url=BASE_URL
)