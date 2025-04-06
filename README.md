# Document-RAG

Setup Instructions
1) Clone the repository : git clone https://github.com/Umesh94kr/Document-RAG
2) Install requirements and packages : pip install requirements.txt
3) In ingest_docs.py and RAG.py just change Chroma client path 'directory_path/ChromaDB'
4) In .env provide your api_key
5) run main.py

Get the server http://127.0.0.1:5000

It contains two endpoints : 
1) Upload PDF
   http://127.0.0.1:5000/upload_PDF
   Open POSTMAN for testing and select POST as request, in Body select form-data and write key as 'file' and select File type
   In the value select PDF from local machine and hit the send button
   
   <img width="1437" alt="Screenshot 2025-04-06 at 8 53 06 AM" src="https://github.com/user-attachments/assets/6402b760-40a7-4651-815d-e9fd9dd45d76" />
   You'll get a response as "emebeddings are successfully created"

2) chat
   http://127.0.0.1:5000/chat
   Open POSTMAN for testing and select POST as request, in Body select raw, keep the payload like below just change the query
   {
    "data" : {
        "query" : "Tell me about text to image synthesis process"
    }
}
   <img width="1440" alt="Screenshot 2025-04-06 at 8 57 04 AM" src="https://github.com/user-attachments/assets/60dae27b-b924-4816-966d-381dbbef4da2" />
