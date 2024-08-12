from django.shortcuts import render
from django.http import HttpResponse
import os
from django.http import JsonResponse
from langchain_community.document_loaders import PyMuPDFLoader
from django.conf import settings
import requests
import json
# import os
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from langchain_community.document_loaders import PyMuPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from langchain_groq import ChatGroq
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_core.prompts import ChatPromptTemplate

# # Ensure to set your Groq API key here
# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# groq_api_key = "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"
# pdf_path = "/Users/anand/openai/M-618.pdf"

# # Load and process the PDF document
# loader = PyMuPDFLoader(pdf_path)
# documents = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
# texts = text_splitter.split_documents(documents)

# embeddings = HuggingFaceEmbeddings()
# index = FAISS.from_documents(texts, embeddings)
# retriever = index.as_retriever()

# llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# prompt = ChatPromptTemplate.from_template(
#     """
#     Answer the questions based on the provided context only.
#     Please provide the most accurate response based on the question.
#     <context>
#     {context}
#     <context>
#     Questions: {input}
#     """
# )

# document_chain = create_stuff_documents_chain(llm, prompt)
# retrieval_chain = create_retrieval_chain(retriever, document_chain)

# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         user_message = request.POST.get('message')
#         if not user_message:
#             return JsonResponse({'error': 'No message provided'}, status=400)
        
#         try:
#             response = retrieval_chain.invoke({'input': user_message})
#             return JsonResponse({'message': response['answer']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


# Create your views here.
def index(request):
    return render(request, "index.html")


def timeline(request):
    return render(request, "timeline.html")


def about(request):
    # pdf_file_path = '/Users/anand/openai/FinalText-FairHousingRegulations.pdf'

    # loader = PyMuPDFLoader(pdf_path)
    # documents = loader.load()

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    # texts = text_splitter.split_documents(documents)

    # # Extract text from PDF using PyMuPDFLoader
    # loader = PyMuPDFLoader(pdf_file_path)
    # documents = loader.load()
    # pdf_text = "\n".join([doc.page_content for doc in documents])

    # groq_api_key = "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"
    # groq_api_url = "https://api.groq.com/openai/v1/chat/completions"  # Replace with actual Groq API endpoint

    # # Set up the request payload
    # payload = {
    #     "model": "llama3-70b-8192",  # Replace with the actual model identifier if needed
    #     "prompt": pdf_text
    # }

    # headers = {
    #     "Authorization": f"Bearer {groq_api_key}",
    #     "Content-Type": "application/json"
    # }

    # # Make the API request
    # response = requests.post(groq_api_url, json=payload, headers=headers)

    # if response.status_code == 200:
    #     groq_response = response.json().get("choices", [{}])[0].get("text", "No response")
    # else:
    #     groq_response = "Error: Unable to fetch response from Groq API."

    # return JsonResponse({'pdf_text': pdf_text, 'groq_response': groq_response})
    return render(request, "about.html")


def profile(request):
    return render(request, "profile.html")


def preview(request):
    context = {}
    if "module" in request.GET:
        context["module"] = request.GET.get("module")
        context["module_title"] = " ".join(request.GET.get("module").split("-")).title()
    return render(request, "preview.html", context)


def module(request):
    context = {}
    if "module" in request.GET:
        context["module"] = request.GET.get("module")
        context["module_title"] = " ".join(request.GET.get("module").split("-")).title()
        context["module_file_name"] = context["module"] + ".pdf"
    return render(request, "module.html", context)
