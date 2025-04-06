from flask import Flask, request
import io
from pypdf import PdfReader
from ingest_docs import ingest
from RAG import RAG

app = Flask(__name__)

@app.route("/upload_PDF", methods=["POST", "GET"])
def upload_PDF():
    file = request.files["file"]
    
    reader = PdfReader(io.BytesIO(file.read()))
    ingest_cls = ingest('Collection', '/Users/umesh/Desktop/Terrabase_project/ChromaDB')
    ingest_cls.main(reader, file)

    return {
        "output" : "Embeddings successfully created!!!"
    }

@app.route("/chat", methods=["POST", "GET"])
def chat():
    data = request.get_json()
    query = data['data']['query']

    rag = RAG()
    rag.setup_db()
    chain = rag.answer_question()

    response, contexts = rag.get_response(chain, query)

    return {
        "response" : response['output']
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)

