# ui.py
import streamlit as st
import requests

st.title("🧸 吉伊卡哇小幫手")

st.image("C:/Users/HP/Downloads/RAG/chiikawa.png", width=150)

query = st.text_input("想問什麼呢…？")

if query:
    try:
        res = requests.get("http://127.0.0.1:8000/ask", params={"query": query})
        
        # 調試：顯示狀態碼和原始響應
        st.write(f"🔍 狀態碼: {res.status_code}")
        # st.write(f"📝 原始響應: {res.text[:200]}")  # 顯示前 200 字
        
        if res.status_code == 200:
            data = res.json()
            st.success(data["answer"])
        else:
            st.error(f"❌ 後端錯誤 ({res.status_code}): {res.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ 無法連接到伺服器！請確認 FastAPI 有啟動 (uvicorn app:app --reload)")
    except Exception as e:
        st.error(f"❌ 發生錯誤：{str(e)}")