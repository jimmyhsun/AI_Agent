import os
from dotenv import load_dotenv
from tts import play_sound
from stt_s3 import speech_to_text
from count_people import count_people
from google import genai
import speech_recognition as sr

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def ai_agent():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("請說話...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="zh-TW")
        print("轉換後文字:", text)

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=text
        )
        print("AI 回覆:", response.text)
        reply = response.text
    except Exception as e:
        reply = "辨識失敗"
        print("辨識失敗:", str(e))

    if "播放聲音" in reply or "喇叭" in reply or "讓喇叭發聲" in reply:
        play_sound("這是一個測試音效")
    elif "語音轉文字" in reply or "stt" in reply or "STT" in reply:
        speech_to_text()
    elif "人數" in reply or "鏡頭" in reply:
        count_people()
    else:
        print("無法識別指令")

ai_agent()
