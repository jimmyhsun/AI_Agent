import speech_recognition as sr
import boto3
import os

# AWS S3 設定
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")

def upload_to_s3(file_path, s3_key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    s3.upload_file(file_path, S3_BUCKET_NAME, s3_key)
    print(f"檔案 {file_path} 已上傳至 S3")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("請說話...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="zh-TW")
        print("轉換後文字:", text)

        # 儲存音訊和文字檔
        with open("speech.wav", "wb") as f:
            f.write(audio.get_wav_data())

        with open("speech.txt", "w", encoding="utf-8") as f:
            f.write(text)

        #  上傳到 S3
        upload_to_s3("speech.wav", "speech.wav")
        upload_to_s3("speech.txt", "speech.txt")

    except Exception as e:
        print("辨識失敗:", str(e))

# speech_to_text()
