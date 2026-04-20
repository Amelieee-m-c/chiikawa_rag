# 🧸 Chiikawa RAG Assistant

## Features
- Retrieval-Augmented Generation (RAG)
- Persona-based response (Chiikawa style)
- Source-grounded answers

## Tech Stack
- LangChain
- FAISS
- OpenAI API
- Streamlit

- test_model.py 可以看目前你的API有支援那些模型
- app.py 整個流程架構串接
- db.py 存到SQL裡面
- llm.py 看你要用哪個模型，去套用他的API
- prompt.py 針對吉伊卡哇這個角色，賦予它角色設定
- rag.py
- sample.txt
- ui.py 前端介面