import pyttsx3

def play_sound(text="播放聲音"):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# play_sound("你好，我是你的 AI 助手")