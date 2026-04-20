# app.py
from fastapi import FastAPI
import datetime

from rag import retrieve
from llm import ask_llm
from db import init_db, save_chat
from prompt import CHIikawa_PROMPT

app = FastAPI()
init_db()

@app.get("/ask")
def ask_api(query: str):

    # 1️⃣ RAG
    context = retrieve(query)

    # 2️⃣ 組prompt（改善版）
    if context.strip():
        # 有搜到資料
        full_prompt = CHIikawa_PROMPT + f"\n\n【我找到的資料】\n{context}\n\n【用戶問題】\n{query}"
    else:
        # 沒搜到資料，允許自由回答
        full_prompt = CHIikawa_PROMPT + f"\n\n【提示】資料庫沒有相關資料，但你可以用你的知識回答。\n\n【用戶問題】\n{query}"
        #gemini回答

    # 3️⃣ LLM
    answer = ask_llm(full_prompt)

    # 4️⃣ 存SQL（你原本的核心）
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_chat(query, answer, now)

    return {
        "question": query,
        "answer": answer,
        "time": now
    }