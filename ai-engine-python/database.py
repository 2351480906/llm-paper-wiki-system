import chromadb
from chromadb.utils import embedding_functions
from config import QWEN_API_KEY, BASE_URL

# 初始化阿里云的文本转向量模型
dashscope_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=QWEN_API_KEY,
    api_base=BASE_URL,
    model_name="text-embedding-v3"
)

# 连接本地持久化向量库
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="research_papers",
    embedding_function=dashscope_ef
)


def add_documents_to_db(chunks, filename):
    """处理阿里云限流，分批将数据写入数据库"""
    if not chunks: return

    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename} for _ in chunks]
    batch_size = 10

    for i in range(0, len(chunks), batch_size):
        collection.add(
            documents=chunks[i: i + batch_size],
            metadatas=metadatas[i: i + batch_size],
            ids=ids[i: i + batch_size]
        )
def delete_documents_by_source(filename):
    """清理属于某篇文献的所有旧向量数据"""
    try:
        # 通过 metadata 里的 source 字段精准狙击并删除
        collection.delete(where={"source": filename})
        print(f"🧹 [Database] 成功清理 {filename} 的旧向量数据")
    except Exception as e:
        print(f"⚠️ [Database] 清理旧向量数据跳过或失败: {str(e)}")