import os
import chromadb
import json
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from prompts import qa_prompt
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

class RAG:
    """
    RAG class for setting up the RAG pipeline
    """
    
    def __init__(self):
        self.embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.vector_db = None
        self.retriever = None
        self.qa_prompt = qa_prompt


    def setup_db(self):
        """
        Initializes the retriever for ChromaDB
        """

        client = chromadb.PersistentClient(path="/Users/umesh/Desktop/Terrabase_project/ChromaDB")
        self.vector_db = Chroma(
            client=client,
            collection_name="Collection",
            embedding_function= self.embedding_function
            )    
        self.retriever = self.vector_db.as_retriever(search_type='mmr') 


    def answer_question(self):
        """
        Creates a chain that can answer questions
        """
        question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
        rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)
        return rag_chain


    def get_response(self, chain, query):
        """
        Invokes the RAG chain for response
        """

        response = chain.invoke({"input": query})
        answer = json.loads(response['answer'])
        context = response['context']

        return answer, context
        

if __name__ == "__main__":  
    rag = RAG()
    rag.setup_db()
    chain = rag.answer_question()
    print("------------------------------------------------------\nEnter your query(q for exit): \n")

    while True:
        query = input("User: ")
        if query.lower()=='q':
            print("\nChat finished. Have nice day!")
            break
        response, contexts = rag.get_response(chain, query)
        print("ChatBot: " + response['output'] + '\n')
        for context in contexts:
            print(context)
        print("-------------------------------------------")
    
    print("------------------------------------------------------")  