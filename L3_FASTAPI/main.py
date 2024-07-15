import traceback
from typing import List, Dict
from fastapi import FastAPI, File, HTTPException, UploadFile, Request, Response,Body
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
# from PyPDF2 import PdfFileReader, PdfFileWriter
import shutil
import io
import sys
import os
import fitz  # PyMuPDF
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.parts import fetch_trial, load_questions_from_cuad, load_model_and_tokenizer, extract_clause_from_question
from components.predictions import run_prediction
from components.deviations import (
    categorize_predictions,
    categorize_predictions_levenshetin,
    categorize_predictions_with_embeddings
)


origins = [
    "*"
]

# app.add_middleware(
#     CORSMiddleware,
#     # allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
            
    )
]

app = FastAPI(middleware=middleware)


print('HI')
# Load model and tokenizer globally
model_path = 'models/roberta-base'
model, tokenizer, device = load_model_and_tokenizer(model_path)

# Load questions globally
cuad_json_path = 'data/CUADv1.json'
questions = load_questions_from_cuad(cuad_json_path)

class ComparisonResult(BaseModel):
    additions: list
    subtractions: list
    potential_modifications: list

class CompareContractsRequest(BaseModel):
    predictions1: Dict[str, str]  # or Predictions if you define the structure
    predictions2: Dict[str, str]  # or Predictions if you define the structure
    method: str
    
class HighlightRequest(BaseModel):
    file_name: str
    additions: list
    subtractions: list
    modifications: list

@app.get("/analyze_contract")
def testing():
    print("testing works")
    return "Hi your testing is working"

# @app.post("/analyze_contract")
# async def analyze_contract(file_upload:UploadFile = File(...)):
#     # print(type(file))
#     # print("Inisde analyze_contract")
#     # # contents = await file.read()
#     # print("Before ET")
#     # print(type(file_upload))
#     # print(file_upload)
#     # contract_text= upload_convert(file_upload)
#     # if contract_text=='content is empty':
#     #     return JSONResponse(content={"error": "Empty file content"}, status_code=400)
#     # # contract_text = extract_text_from_pdf(filepath)
#     # elif not contract_text:
#     #     return JSONResponse(content={"error": contract_text}, status_code=500)
        
#     # print("After Upload Convert")
#     # # print(contract_text.keys())
#     # predictions = run_prediction(questions, contract_text, model, tokenizer, device)
#     # print("After P")
#     # return {"predictions": predictions}
    
#     # Check if the uploaded file is a PDF
#     type_check = typeOfUpload(file_upload)
#     if isinstance(type_check, JSONResponse):
#         return type_check
    
#     # stores it in the local system
#     #! can change this to a db!!!   
#     path = f"contracts/{file_upload.filename}"
#     print("path is",path)
#     with open(path,"wb+") as file:
#         shutil.copyfileobj(file_upload.file,file)
        
#     return {
#         'file':file_upload.filename,
#         'content':file_upload.content_type,
#         'path':path
#     }


@app.post("/analyze_contract")
async def analyze_contract(file_upload: UploadFile = File(...)):
    print('Within Analyze Contract')
    try:
        # Check if the uploaded file is a PDF
        type_check = typeOfUpload(file_upload)
        if isinstance(type_check, JSONResponse):
            return type_check
        

        # print("Before extracting text")
        # Extract text from the PDF file
        contract_text = extract_text_from_pdf(file_upload)
        
        if not contract_text:
            # print("contract_text is empty")
            return JSONResponse(content={"error": "Failed to extract text from PDF"}, status_code=500)
        # print("After extracting text")
        
        # Reset the file pointer to the beginning of the file
        file_upload.file.seek(0)
        
        path = f"contracts/{file_upload.filename}"
        print("path is",path)
        with open(path,"wb+") as file:
            shutil.copyfileobj(file_upload.file,file)
        
        print("this is the ", device)
        
        predictions_dict = run_prediction(questions, contract_text, model, tokenizer, device)

        # # Debugging prints
        # print(f"Number of questions: {len(questions)}")
        # print(f"Number of predictions: {len(predictions_dict)}")

        # Ensure predictions_dict keys are strings
        # predictions_list = [predictions_dict[str(i)] for i in range(len(questions))]
        
        # Extract clauses from questions
        clauses = [extract_clause_from_question(question) for question in questions]
        
        # Construct a dictionary of clauses and predictions
        predictions = {clauses[i]: predictions_dict[str(i)] for i in range(len(questions))}        

        
        # Construct response
        response = {
            'file': file_upload.filename,
            # 'content': file_upload.content_type,
            # 'extracted_text': contract_text,
            'predictions': predictions
        }
        
        print("respoonse to analyze_contract is", response)
        # print("Response:", response)
        
        return response
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()  # Print the full traceback
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)
    

def extract_text_from_pdf(file_upload: UploadFile):
    try:
        # Read the file content
        pdf_content = file_upload.file.read()
        # print("PDF content read successfully")

        # Use PyMuPDF to extract text
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        # print(f"Number of pages in the document: {len(doc)}")
        
        text = ""
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            # print(f"Text from page {page_num + 1}: {page_text[:100]}")  # Print first 100 characters of each page
            text += page_text
        
        # print("Text extraction successful")
        return text
    except Exception as e:
        print(f"Error during text extraction: {e}")
        # traceback.print_exc()  # Print the full traceback
        return None


    
def typeOfUpload(file_upload:UploadFile = File(...) ):
    if file_upload.content_type != "application/pdf":
        return JSONResponse(content={"error": "Invalid file type. Only PDF files are allowed."}, status_code=400)


# def upload_convert(upload):
#     contract_text= upload.file.read()
#     # print(f"contract_text length: {len(contract_text)}") # Print length for debugging
#     # if not contract_text:
#     #     return "content is empty"
#     print("contracy_text within funvtion is",contract_text[0:100])
#     try:
#         pdf_reader = PdfFileReader(io.BytesIO(contract_text))
#         text = ""
#         for page_num in range(pdf_reader.getNumPages()):
#             text += pdf_reader.getPage(page_num).extractText()
#         print("TEXT IS OFF THE FORM",pdf_reader.getPage(page_num).extractText())
#         return text
#     except Exception as e:
#         print("inside testing error")
#         return e


# @app.post("/compare_contracts")
# async def compare_contracts(
#     # file1: UploadFile = File(...),
#     predictions1:dict ,
#     predictions2:dict ,
#     # file2: UploadFile = File(...),
#     method: str = "jaccard"
# ):
#     # contents1 = await file1.read()
#     # contents2 = await file2.read()
    
#     # contract_text1 = extract_text_from_pdf()
#     # contract_text2 = extract_text_from_pdf()
    
#     # predictions1 = run_prediction(questions, contract_text1, model, tokenizer, device)
#     # predictions2 = run_prediction(questions, contract_text2, model, tokenizer, device)
    
#     if method == "jaccard":
#         additions, subtractions, potential_modifications = categorize_predictions(predictions1, predictions2)
#     elif method == "levenshtein":
#         additions, subtractions, potential_modifications = categorize_predictions_levenshetin(predictions1, predictions2)
#     elif method == "bert":
#         additions, subtractions, potential_modifications = categorize_predictions_with_embeddings(predictions1, predictions2)
#     else:
#         return {"error": "Invalid comparison method"}
    
#     return ComparisonResult(
#         additions=additions,
#         subtractions=subtractions,
#         potential_modifications=potential_modifications
#     )
    
@app.post("/compare_contracts2")
async def compare_contracts2(request: CompareContractsRequest = Body(...)) -> ComparisonResult:
    predictions1 = request.predictions1
    predictions2 = request.predictions2
    method = request.method

    if method == "jaccard":
        additions, subtractions, potential_modifications = categorize_predictions(predictions1, predictions2)
    elif method == "levenshtein":
        additions, subtractions, potential_modifications = categorize_predictions_levenshetin(predictions1, predictions2)
    elif method == "bert":
        additions, subtractions, potential_modifications = categorize_predictions_with_embeddings(predictions1, predictions2)
    else:
        raise ValueError("Invalid comparison method")
    
    return ComparisonResult(
        additions=additions,
        subtractions=subtractions,
        potential_modifications=potential_modifications
    )
    
# @app.post("/highlight_deviations")
# async def highlight_deviations(request: Request):
#     print("within function")
#     try:
#         payload = await request.json()
#         print(f"Received payload: {payload}")

#         highlight_request = HighlightRequest(**payload)
#         print(f"Parsed request data: {highlight_request.dict()}")

#         pdf_path = f"contracts/{highlight_request.file_name}"
#         print("pdf_path is ", pdf_path)

#         if not os.path.exists(pdf_path):
#             print("file not found")
#             raise HTTPException(status_code=404, detail="File not found")

#         def highlight_text_in_pdf(pdf_path, highlights, color):
#             doc = fitz.open(pdf_path)
#             for page_num in range(len(doc)):
#                 page = doc.load_page(page_num)
#                 for highlight in highlights:
#                     if not isinstance(highlight, str):
#                         print(f"Invalid highlight: {highlight}")
#                         continue
#                     text_instances = page.search_for(highlight)
#                     for inst in text_instances:
#                         highlight = page.add_highlight_annot(inst)
#                         highlight.set_colors(stroke=color)
#                         highlight.update()
#             output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
#             doc.save(output_path)
#             print("output path is", output_path)
#             return output_path

#         highlighted_path = highlight_text_in_pdf(pdf_path, highlight_request.additions, (0, 1, 0))
#         highlighted_path = highlight_text_in_pdf(highlighted_path, highlight_request.subtractions, (1, 1, 0))
#         highlighted_path = highlight_text_in_pdf(highlighted_path, highlight_request.modifications, (1, 0, 0))

#         return FileResponse(highlighted_path, media_type="application/pdf", filename=f"{highlight_request.file_name}_highlighted.pdf")
#     except Exception as e:
#         print(f"Error highlighting deviations: {e}")
#         traceback.print_exc()
#         return JSONResponse(content={"error": "Failed to highlight deviations"}, status_code=500)

@app.post("/highlight_deviations")
async def highlight_deviations(request: Request):
    print("within function")
    try:
        payload = await request.json()
        print(f"Received payload: {payload}")

        highlight_request = HighlightRequest(**payload)
        print(f"Parsed request data: {highlight_request.dict()}")

        pdf_path = f"contracts/{highlight_request.file_name}"
        print("pdf_path is ", pdf_path)

        if not os.path.exists(pdf_path):
            print("file not found")
            raise HTTPException(status_code=404, detail="File not found")

        def highlight_text_in_pdf(pdf_path, highlights, color):
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                for highlight in highlights:
                    # Assuming highlight is a tuple where the second element is the text to be highlighted
                    text = highlight[1]
                    text_instances = page.search_for(text)
                    for inst in text_instances:
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=color)
                        highlight.update()
            output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
            doc.save(output_path)
            print("output path is", output_path)
            return output_path

        highlighted_path = highlight_text_in_pdf(pdf_path, highlight_request.additions, (0, 1, 0))
        highlighted_path = highlight_text_in_pdf(highlighted_path, highlight_request.subtractions, (1, 1, 0))
        os.remove(highlighted_path.replace("_highlighted.pdf", ".pdf"))
        highlighted_path = highlight_text_in_pdf(highlighted_path, highlight_request.modifications, (1, 0, 0))
        os.remove(highlighted_path.replace("_highlighted.pdf", ".pdf"))


        return FileResponse(highlighted_path, media_type="application/pdf", filename=f"{highlight_request.file_name}_highlighted.pdf")
    except Exception as e:
        print(f"Error highlighting deviations: {e}")
        traceback.print_exc()
        return JSONResponse(content={"error": "Failed to highlight deviations"}, status_code=500)

@app.post("/fetch_trial")
async def trial():
    a=fetch_trial()
    print(a)
    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)