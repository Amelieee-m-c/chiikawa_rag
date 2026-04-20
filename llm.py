import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. 務必加上這行，才會去讀取你的 .env 檔案
load_dotenv()

# 2. 從環境變數抓取金鑰，不要寫預設值
api_key = os.getenv("GOOGLE_API_KEY")

# 3. 檢查金鑰是否存在，這是一個專業的防錯機制
if not api_key:
    raise ValueError("找不到 GOOGLE_API_KEY！請確認 .env 檔案內容正確。")

genai.configure(api_key=api_key)

# 4. 改用
model = genai.GenerativeModel("models/gemini-2.5-flash")

def ask_llm(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"呼叫 Gemini 時發生錯誤：{str(e)}"