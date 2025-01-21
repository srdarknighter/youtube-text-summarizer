# youtube-text-summarizer

# A brief about the steps followed:

1. Used the pegasus trained on the cnn dataset as the base model
2. Fine tuned it with samsum dataset, this consists of dialogue and its corresponding summary
3. Generated rouge-1, rouge-2, rougeL and rougeLSum scores for a dataset that made a summary of short paras from hugging face. Dataset Link: seanfu112/youtube_video_summaries
4. Insights from rouge scores:
   a. Rouge-1 score was hovering around 0.45 ish which is considered pretty good
   b. Rouge-2 score saw a sharp dip in performance averaged around 0.27 which is very low. Generally, 0.4 and above indicates that it is unable to capture the overlap of bigrams.
   c. Rouge-L score was 0.34 - satisfactory
   d. Rogue-Lsum score 0.34 - satisfactory


Output Sample:
![image](https://github.com/user-attachments/assets/c3111ebf-25c7-4a50-8766-d579abc83ce2)


Logs also didnt provide any comments on the error faced
Link: https://youtube-text-summarizer.streamlit.app/
![image](https://github.com/user-attachments/assets/72c4b617-d4cc-4494-8b59-ceef0066f43d)  ---- Error picture
