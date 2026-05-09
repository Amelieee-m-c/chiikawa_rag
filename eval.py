import os
import json
from google import genai 
from google.genai import types
from rag import retrieve
from llm import ask_llm
from dotenv import load_dotenv

load_dotenv()

# ✅ 修正點 1：必須透過 genai.Client 調用，因為你是使用 from google import genai
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
JUDGE_MODEL_ID = "gemini-2.5-flash" 

test_cases = [
    {"query": "葉子變黃的原因有哪些？", "expected": "缺氮、澆水過多、病害或光照不足"},
    {"query": "如何照顧玫瑰？", "expected": "充足日照、排水良好、定期施肥，澆水澆根部"},
    {"query": "什麼是 RAG？", "expected": "檢索增強生成，結合搜尋與模型回答"},
    {"query": "燙傷如何處理？", "expected": "（應回答不確定，因為資料庫無此資訊）"}
]

def judge_answer(query, context, answer):
    prompt = f"""
    你是一位專業的 AI 評測員。請根據以下【參考資料】評估【AI 的回答】。
    
    【用戶問題】：{query}
    【參考資料】：{context}
    【AI 的回答】：{answer}
    
    請針對以下兩個指標給分（1-5分，5分最高）：
    1. 忠實度 (Faithfulness)：回答是否完全根據參考資料？有無編造內容？
    2. 相關性 (Relevance)：回答是否直接解決了用戶的問題？
    """
    
    try:
        # ✅ 修正點 2：加入 config 設定輸出格式為 JSON，這能省去手動清理 ```json 的麻煩
        response = client.models.generate_content(
            model=JUDGE_MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "faithfulness": {"type": "INTEGER"},
                        "relevance": {"type": "INTEGER"},
                        "reason": {"type": "STRING"}
                    }
                }
            )
        )
        
        # 直接解析返回的 JSON 文字
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

def run_evaluation():
    print("--- 🧸 吉伊卡哇 RAG 系統評測 (New SDK 版) ---")
    results = []
    
    for case in test_cases:
        query = case["query"]
        # 從你的 rag.py 抓取檢索內容[cite: 10]
        context = retrieve(query) 
        # 從你的 llm.py 產出回答[cite: 3, 7]
        answer = ask_llm(f"請根據資料回答：{query}\n資料：{context}") 
        
        score = judge_answer(query, context, answer)
        
        report = {
            "query": query,
            "answer": answer,
            "expected": case["expected"],
            "evaluation": score
        }
        results.append(report)
        print(f"Q: {query}\nScore: {score}\n{'-'*30}")

    with open("eval_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("✅ 評測完成！報告已儲存至 eval_report.json")

if __name__ == "__main__":
    run_evaluation()