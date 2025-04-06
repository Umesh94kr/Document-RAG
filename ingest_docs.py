from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb.utils.embedding_functions as embedding_functions
import urllib.parse
import chromadb
import nest_asyncio
import os
from dotenv import load_dotenv
import requests
import io
from pypdf import PdfReader
import re
from uuid import uuid4

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

class ingest:
    """
    Ingestor class for loading documents chunking them, embedding them, and storing them in ChromaDB
    """

    def __init__(self, collection_name, path):
        self.chunk_size = 700
        self.chunk_overlap = 100
        self.client = chromadb.PersistentClient(path='/Users/umesh/Desktop/Terrabase_project/ChromaDB')
        self.collection = "Collection"
        self.embedding_func = embedding_functions.OpenAIEmbeddingFunction(api_key=os.environ["OPENAI_API_KEY"], model_name="text-embedding-3-small")

    def load_pdf(self, reader, file):
        """Extracts text from a PDF file and returns semantic chunks."""

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        #with open(pdf_path, "rb") as file:
        #    reader = PdfReader(file)

        text = ""
            
        for i, page in enumerate(reader.pages):
            text += page.extract_text() or ""

        chunks = text_splitter.split_text(text)

        chunks_mdata = []
        for chunk in chunks:
            data = {
                "text" :chunk,
                "metadata" : {
                    "filename" : file.filename
                    }
            }
            chunks_mdata.append(data)
        
        return chunks_mdata
    
    def embed_and_store(self, texts):
        """
        Embeds the chunks and stores them in the collection
        """

        #collection = self.client.create_collection(name=self.collection, metadata={"hnsw:space": "cosine"}, embedding_function=self.embedding_func)
        collection = self.client.get_or_create_collection(name=self.collection, embedding_function=self.embedding_func)

        # Extract content, metadata, and IDs sequentially
        documents = [chunk['text'] for chunk in texts]
        metadatas = [chunk['metadata'] for chunk in texts]
        ids = [str(i) for i in range(len(texts))]

        # Sequentially add documents to the collection
        print(f'🔃 Adding embeddings to {self.collection}...\n')
        for doc, meta, doc_id in zip(documents, metadatas, ids):
            collection.add(documents=[doc], metadatas=[meta], ids=[doc_id])

        print(f'✅ Embeddings added to {self.collection}!\n')


    def main(self, reader, file):
        """
        Main function to run the ingestor
        """
        chunks_primary = self.load_pdf(reader, file)
        #print(chunks_primary[0]["text"])
        #print(chunks_primary)
        #return chunks_primary
        self.embed_and_store(chunks_primary)


#if __name__ == "__main__":
#    print("------------------------------------------------------\n")

#    path = input("Path to ChromaDB :")
#    collection_name = input("Name your collection : ")
#    ingest = ingest(collection_name, path)
#    ingest.main('/Users/umesh/Desktop/Terrabase_project/2301.09515v1.pdf')

#    print("\n------------------------------------------------------")
