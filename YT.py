import langchain
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate

from langchain.chains import LLMChain
import ollama
from langchain_community.llms import Ollama
import youtube_transcript_api

from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.docstore.document import Document
from langchain_ollama import OllamaEmbeddings

# Default model is 'nomic-embed-text', or specify a different one
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
import re

def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from full URL formats.
    """
    
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})"
    ]
    
    for p in patterns:
        match = re.search(p, url)
        if match:
            return match.group(1)

    raise ValueError("Could not extract video ID from URL: " + url)


def create_db_from_youtube_video_url(video_url: str) -> FAISS:
    # Extract video ID
    video_id = extract_video_id(video_url)
    ytt_api = YouTubeTranscriptApi() 
    transcript=ytt_api.fetch(video_id)
    transcript_text = " ".join([segment.text for segment in transcript]) # Wrap in LangChain Document
    document = Document(page_content=transcript_text) 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100) 
    docs = text_splitter.split_documents([document])
    print(docs)
    db = FAISS.from_documents(docs, embeddings) 
    return db
    
    

def get_response(db, query, k=8):
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    l=Ollama(model="gemma3:1b",temperature=0.3)

    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are an information extraction and summarization assistant.

        Your task is to respond using ONLY the provided video transcript.
        First, determine the user's intent:
        • If the user asks to "summarize", "summarise", or requests a summary, treat it as a SUMMARY task.
        • Otherwise, treat it as a QUESTION-ANSWERING task.
        

        STRICT RULES (must follow all):
        1. Use ONLY information explicitly present in the transcript.
        2. Do NOT use prior knowledge, assumptions, or external information.
        3. Do NOT infer or guess beyond the transcript.
        4. If the request is a QUESTION and the transcript does not contain enough information,
        respond exactly with: "I don't know."
        5. If the request is a SUMMARY, generate the summary ONLY from the transcript.
        6. If a word or sentence limit is specified, strictly follow it.
        7. For summaries:
        • Capture main themes, key points, and conclusions
        • Do NOT add opinions or missing details
        • Do NOT speculate
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        """
        
        
    )

    chain = LLMChain(llm=l, prompt=prompt)

    response = chain.run(question=query, docs=docs_page_content)
    response = response.replace("\n", "")
    
    return response, docs


