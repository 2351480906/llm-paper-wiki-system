from pydantic import BaseModel
from typing import List

class SettingsConfig(BaseModel):
    base_path: str
    llm_model: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class MergeWikiRequest(BaseModel):
    filename: str
    question: str   
    answer: str

class SaveWikiRequest(BaseModel):
    topic: str
    content: str