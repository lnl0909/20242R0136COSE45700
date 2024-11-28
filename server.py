from flask import Flask, request, send_file
import os
import random
import requests

app = Flask(__name__)

@app.route('/process-youtube', methods=['POST'])
def process_youtube():
    # 1. 유튜브 링크 받기
    data = request.json
    youtube_url = data.get("youtube_url")
    if not youtube_url:
        return {"error": "No YouTube URL provided"}, 400

    # 2. 다운로드 및 처리 로직 실행
    # (여기에 앞서 설명한 다운로드 및 온셋 탐지, 파일 생성 코드가 포함됨)

    # 파일 이름
    output_file = "modified_vocal_onset_times.txt"

    # 3. Unity로 파일 전송
    if os.path.exists(output_file):
        return send_file(output_file, as_attachment=True)
    else:
        return {"error": "Processed file not found"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)