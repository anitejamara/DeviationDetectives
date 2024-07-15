import fitz  # PyMuPDF
import json 
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from PyPDF2 import PdfFileReader, PdfFileWriter
import io
import re


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def load_questions_from_cuad(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
    questions = [q['question'] for q in data['data'][0]['paragraphs'][0]['qas']]
    return questions


def load_model_and_tokenizer(model_path):
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    return model, tokenizer, device

# def upload_convert(upload):
#     contract_text= upload.read()
#     # print(f"contract_text length: {len(contract_text)}") # Print length for debugging
#     # if not contract_text:
#     #     return "content is empty"
#     try:
#         pdf_reader = PdfFileReader(io.BytesIO(contract_text))
#         text = ""
#         for page_num in range(pdf_reader.getNumPages()):
#             text += pdf_reader.getPage(page_num).extractText()
#         print("TEXT IS OFF THE FORM",pdf_reader.getPage(page_num).extractText())
#         return text
#     except Exception as e:
#         return {'error':e}
    
def fetch_trial():
    return ("the fetch is working")


def extract_clause_from_question(question):
    clause_pattern = r'related to "(.*?)"'
    match = re.search(clause_pattern, question)
    return match.group(1) if match else None


     
    
    
    
