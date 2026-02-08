# YT_Insight
<img width="1898" height="674" alt="image" src="https://github.com/user-attachments/assets/bdad0bc5-055a-4bf8-a100-f88f912f6679" />
An example of an AI-generated summary produced by the YouTube Insight project, demonstrating how long YouTube videos can be condensed into clear and informative text. The summary is generated solely from the video transcript, making it especially useful for getting a quick glimpse of the content spoken by the speaker without watching the entire video.Additionally, users can ask questions about the  content, and the system responds based only on the transcript-if a topic is not spoken about in the video, the system clearly indicates that the information is not present.

# 1️⃣ Project Overview
YouTube Insight is an AI-powered tool that helps users quickly understand YouTube videos by generating summaries and answering questions based on the video transcript. It is designed for users who want fast insights without watching long videos end-to-end.

# 2️⃣ Key Features 
🎯 Transcript-based video summarization

💬 Question answering strictly from spoken content

❌ Clearly indicates when information is not present in the video

⚡ Fast and lightweight analysis

🧠 Prevents hallucinations by limiting responses to transcript data

# 3️⃣ How It Works (Technical but simple)

Fetches the YouTube video transcript
Processes transcript text
Uses RAG and Generates a concise summary using an AI model
Answers user questions by matching them against transcript content
Returns “I don't know” when relevant data is missing

# 4️⃣ Tech Stack

Language: Python / JavaScript
AI Model:gemma3:1b
APIs:YouTubeTranscriptApi
Frontend: Streamlit 
Backend:Python
Langchain
Ollama

# 5️⃣ Example Use Cases

Students summarizing long lectures
Interview preparation from podcasts or talks
Quick content screening for researchers
Accessibility for users with limited time

# 6️⃣ Limitations (This impresses reviewers)

Works only with videos that have available transcripts
Visual content (slides, diagrams) is not analyzed
Accuracy depends on transcript quality

# 7️⃣ Future Improvements

Support for multilingual transcripts
Timestamp-based answers
Improved semantic search over transcripts

8️⃣ Installation & Usage
git clone https://github.com/Megh2004/YT_Insight
cd YT_Insight
streamlit run app.py
