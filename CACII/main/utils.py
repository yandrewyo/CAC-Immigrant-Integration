import os
import ssl
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pathlib import Path

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

os.environ["TOKENIZERS_PARALLELISM"] = "false"
groq_api_key = ""

BASE_DIR = Path(__file__).resolve().parent.parent

def extract_keywords(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    keywords.append("document")
    return keywords

def check_document_relevance(retrieved_docs, user_prompt):
    if not retrieved_docs:
        return False
    doc_texts = [doc.page_content for doc in retrieved_docs]
    keywords = extract_keywords(user_prompt.lower())
    for k in keywords:
        for doc_text in doc_texts:
            if k in doc_text.lower():
                return True
    return False    

def get_response(user_prompt,filename):
    pdf_path = str(BASE_DIR) + '/static/' + filename

    # Load and process the document
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    nltk.download('stopwords')
    nltk.download('punkt')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    texts = text_splitter.split_documents(documents)

    # Use FAISS vector DB
    embeddings = HuggingFaceEmbeddings()
    index = FAISS.from_documents(texts, embeddings)
    retriever = index.as_retriever()

    # Set up the LLM
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the questions based on the provided context only.
        Please provide the most accurate response based on the question.
        %- if context -%
        <context>
        {context}
        </context>
        %- endif -%
        Questions: {input}
        """
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({'input': user_prompt})
    retrieved_docs = retriever.invoke(user_prompt)
    if check_document_relevance(retrieved_docs, user_prompt):
        #pdf specific response
        return response['answer']
    else:
        #generic llm response
        response = llm.invoke(user_prompt)
        test = response.pretty_repr()
        return test
