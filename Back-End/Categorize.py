import google.generativeai as genai
import json
from time import sleep
import os
import DivideEvent


api_key = ""
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-pro-002')

def category(combined_data):
    combined_data = json.dumps(combined_data)
    Categorize = model.generate_content("請根據下列多則新聞摘要，將它們分群以識別屬於同一事件的新聞。分群時，請考慮以下依據："
                                "1. 事件描述的相似度（摘要內容）"
                                "2. 關鍵字的重合率"
                                "3. 事件日期是否接近"
                                "4. 重要關鍵人物或地點是否一致"
                                "請以 JSON 格式回傳分群結果，格式範例如下："
                                "{"
                                "'事件名稱1(請你幫忙取名)':{"
                                "Index: [1, 2, 3],"
                                "Summary: ['摘要1', '摘要2', '摘要3'],"
                                "Key: ['關鍵字1', '關鍵字2', '關鍵字3'],"
                                "Date: 'YYYY-MM-DD'"
                                "URL: ['網址1', '網址2', '網址3']"
                                "},"
                                "'事件名稱2(請你幫忙取名)':{"
                                "Index: [4, 5, 6],"
                                "Summary: ['摘要4', '摘要5', '摘要6'],"
                                "Key: ['關鍵字4', '關鍵字5', '關鍵字6'],"
                                "Date: 'YYYY-MM-DD'"
                                "URL: ['網址4', '網址5', '網址6']"    
                                "},"
                                "..."
                                "}"
                                + 
                                "以下是需要請你分類的新聞摘要："
                                +combined_data)
    print("Categorize:", Categorize.text)
    with open("Categorize.json", "w", encoding="utf-8") as file:
        file.write(Categorize.text)
    print("結果已儲存至 Categorize.json")
    return DivideEvent.divide(Categorize.text)
