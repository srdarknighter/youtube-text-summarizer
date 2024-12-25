import streamlit as st
import torch
import transformers
import youtube_transcript_api
from transformers import AutoModelForSeq2SeqLM, PegasusTokenizer, pipeline
import gdown

@st.cache_resource
def load_model():
  url = f'https://drive.google.com/file/d/1-5IVbAXkeY63tdHZrsn4GIj5i8dp9juO/view?usp=drive_link'
  output = 'model_weights.pth'
  gdown.download(url, output, quiet=False)
  tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-cnn_dailymail")
  model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-cnn_dailymail")
  model.load_state_dict(torch.load(output))
  return model, tokenizer

model, tokenizer = load_model()

st.title("Youtube Video Summarizer")

from youtube_transcript_api import YouTubeTranscriptApi
video_id = st.text_input("Enter the Youtube URL: ")
video_id = video_id.split("=")[1]
transcript1 = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
transcript = " ".join([t['text'] for t in transcript1])

if video_id and st.button("Summarize"):
  pipe = pipeline('summarization', model = model, tokenizer = tokenizer)
  pipe_out = ' '
  for i in range(0, len(transcript)//1000+1):
    chunk = transcript[i * 1000:(i + 1) * 1000]
    summary = pipe(chunk, max_length=80, min_length=20, num_beams=4)
    pipe_out += summary + ' '
  st.write("**Summary: **",pipe_out)
