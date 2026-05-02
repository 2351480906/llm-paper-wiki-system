import os
import json
from config import WIKI_DIR
from document_core import load_catalog  # 等下会在 document_core 中定义

def search_local_catalog(keyword: str) -> str:
    """在本地 pdf_catalog.json 中进行智能分词搜索"""
    try:
        catalog = load_catalog()
        results = []
        search_terms = [k.strip().lower() for k in keyword.split() if k.strip()]

        for filename, info in catalog.items():
            search_text = f"{filename} {info.get('summary', '')} {info.get('category', '')}".lower()
            if all(term in search_text for term in search_terms):
                results.append(f"- 文件名: {filename}\n  摘要: {info.get('summary', '无')}\n  路径: {info.get('path', '无')}")

        if results:
            return f"找到了 {len(results)} 篇相关的文献：\n" + "\n".join(results)
        else:
            return f"系统提示：未找到与 '{keyword}' 相关的文献。请立即用自然语言告诉用户没有找到，并建议他们换个关键词。"
    except Exception as e:
        return f"搜索工具运行出错: {str(e)}"

def read_wiki_content(filename: str) -> str:
    """读取指定 Wiki 笔记的全文内容"""
    try:
        if filename.endswith('.pdf'):
            filename = filename.replace('.pdf', '.md')
        elif not filename.endswith('.md'):
            filename += '.md'

        file_path = os.path.join(WIKI_DIR, filename)

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            max_chars = 8000
            if len(content) > max_chars:
                return f"成功读取文献 {filename}，已截取前 {max_chars} 字：\n\n{content[:max_chars]}\n\n...[后续内容已省略]"
            return f"成功读取文献 {filename}，全文如下：\n\n{content}"
        else:
            return f"系统提示：未找到名为 '{filename}' 的 Wiki 笔记。"
    except Exception as e:
        return f"阅读工具运行出错: {str(e)}"

# 工具说明书
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_local_catalog",
            "description": "当用户询问本地知识库中是否有特定主题的内容，或者你需要先查阅目录找相关文献时，调用此工具进行搜索。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "用于搜索的精简关键词，例如 '大模型', 'EEG'"}
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_wiki_content",
            "description": "当且仅当你通过搜索工具知道某篇具体文献的文件名，且用户需要了解具体细节时，调用此工具阅读全文。",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "要阅读的文献文件名，例如 'STA-Net.md'"}
                },
                "required": ["filename"]
            }
        }
    }
]