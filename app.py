from flask import Flask, request, jsonify
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, pipeline
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

MODEL_PATH = 'srdarknighter/model_weights.pth'
TOKENIZER_PATH = "google/pegasus-cnn_dailymail"

model = PegasusForConditionalGeneration.from_pretrained(MODEL_PATH)
tokenizer = PegasusTokenizer.from_pretrained(TOKENIZER_PATH)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:

        data = request.json
        youtube_url = data.get('url', '')
        
        if not youtube_url:
            return jsonify({"error": "No YouTube URL provided"}), 400
        

        video_id = youtube_url.split("v=")[1]
        #extracting transcript of the video
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = " ".join([t['text'] for t in transcript_data])
        

        summarizer = pipeline('summarization', model=model, tokenizer=tokenizer)
        summary_output = ""
        #batching the transcript 
        for i in range(0, len(transcript) // 1000 + 1):
            chunk = transcript[i * 1000:(i + 1) * 1000]
            if chunk.strip():
                summary = summarizer(chunk, max_length=80, min_length=20, num_beams=4)
                summary_output += summary[0]['summary_text'] + " "
        
        return jsonify({"summary": summary_output.strip()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
