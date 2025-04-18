import google.generativeai as genai
import json
from time import sleep
import os
import asyncio

# 設定 API 金鑰
api_key = os.getenv("API_KEY_Gemini")
genai.configure(api_key=api_key)
with open("GenerateNews_EachEvent\\News.json", "r", encoding="utf-8") as f:
    content = f.read()
    content = json.loads(content)
content = content["Content"]

system_instruction = content+"你是在此新聞中的戰爭平民，請你以簡短的幾句話來進行對話式的回答，並請你扮演以下角色，這是他的立場與看法"\
                    ":我們每天都生活在恐懼和不確定之中。戰爭摧毀了我們的生活，奪走了我們的家園和親人。我們渴望和平，希望戰爭儘快結束，讓我們能夠重建我們的生活。我們希望國際社會能夠聽到我們的聲音，並採取行動幫助我們擺脫困境。我們只是想過上正常的生活，讓孩子們能夠在和平的環境中成長。"

system_instruction2 = content+"你是在此新聞中的戰爭平民，請你以簡短的幾句話來進行對話式的回答，並請你扮演以下角色，這是他的立場與看法"\
                    ":我們渴望和平，但也絕不接受任何損害我們主權和領土完整的協議。我們感謝美國的援助，但我們需要更強而有力的安全保障。美俄之間的單獨談判令我們感到擔憂，我們擔心我們的利益會在沒有我們充分參與的情況下被犧牲。我們願意談判，但前提是俄羅斯必須尊重我們的獨立和自決權。我們的人民為自由付出了巨大的代價，我們不會放棄為我們的國家而戰。"

print("Instruction:", system_instruction)
print("Instruction2:", system_instruction2)

# 建立對話模型
model = genai.GenerativeModel('gemini-1.5-pro-002', system_instruction=system_instruction)

model2 =genai.GenerativeModel('gemini-1.5-pro-002', system_instruction=system_instruction2)


# 建立對話歷史 (讓模型記住對話)
chat_session = model.start_chat()
chat_session2 = model2.start_chat()

async def get_user_input():
    """非同步讀取使用者輸入"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, "請輸入你的訊息 (輸入 'exit' 離開)：\n")

async def chat():
    """非同步對話處理"""
    while True:
        message = await get_user_input()
        if message.lower() == "exit":
            break
        
        response = await asyncio.to_thread(chat_session.send_message, message)
        print("Model Response:", response.text)
        sleep(0.5)
        response2 = await asyncio.to_thread(chat_session2.send_message, message)
        print("Model2 Response:", response2.text)
        
        await asyncio.sleep(5)  # 非同步 sleep，不會阻塞主執行緒

if __name__ == "__main__":
    asyncio.run(chat())
