import time
import streamlit as st
import io
import tempfile
import fitz  # PyMuPDF

from components.parts import extract_text_from_pdf, load_questions_from_cuad, load_model_and_tokenizer
from components.predictions import run_prediction
from components.deviations import (
    categorize_predictions,
    categorize_predictions_levenshetin,
    categorize_predictions_with_embeddings
)

# Load model and tokenizer globally
model_path = 'models/roberta-base'  # Update this path
model, tokenizer, device = load_model_and_tokenizer(model_path)

# Load questions globally
cuad_json_path = 'data/CUADv1.json'  # Update this path
questions = load_questions_from_cuad(cuad_json_path)

# Set custom CSS for styling
st.markdown("""
    <style>
    # .stApp {
    #     background-color: #d0cfcfd1;
    # }
    .stButton>button {
        background-color: #0D6EFD;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #005aa7;
        color: white;
    }
    .scroll-container {
        display: flex;
        overflow-x: scroll;
    }
    .scroll-item {
        flex: 0 0 auto;
        margin-right: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Contract Deviation Detection")

uploaded_file1 = st.file_uploader("Choose the first PDF file", type="pdf")
uploaded_file2 = st.file_uploader("Choose the second PDF file", type="pdf")

comparison_method = st.selectbox("Select comparison method", ["jaccard", "levenshtein", "bert"])

analyze_button = st.button("Analyze Contracts")

if analyze_button:
    if uploaded_file1 is not None and uploaded_file2 is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
            tmp1.write(uploaded_file1.read())
            tmp1_path = tmp1.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
            tmp2.write(uploaded_file2.read())
            tmp2_path = tmp2.name

        contract_text1 = extract_text_from_pdf(tmp1_path)
        contract_text2 = extract_text_from_pdf(tmp2_path)

        predictions1 = run_prediction(questions, contract_text1, model, tokenizer, device)
        time.sleep(15)      # for our ensuring this systems hardware does not crash
        predictions2 = run_prediction(questions, contract_text2, model, tokenizer, device)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Predictions for Contract 1")
            for question, answer in predictions1.items():
                st.write(f"Question: {question}")
                st.write(f"Answer: {answer}")
                st.write("")

        with col2:
            st.subheader("Predictions for Contract 2")
            for question, answer in predictions2.items():
                st.write(f"Question: {question}")
                st.write(f"Answer: {answer}")
                st.write("")

    else:
        st.error("Please upload both PDF files")

# detect_button = st.button("Detect Deviations")

# if detect_button:
#     if uploaded_file1 is not None and uploaded_file2 is not None:
#         if comparison_method == "jaccard":
#             additions, subtractions, potential_modifications = categorize_predictions(predictions1, predictions2)
#         elif comparison_method == "levenshtein":
#             additions, subtractions, potential_modifications = categorize_predictions_levenshetin(predictions1, predictions2)
#         elif comparison_method == "bert":
#             additions, subtractions, potential_modifications = categorize_predictions_with_embeddings(predictions1, predictions2)
#         else:
#             st.error("Invalid comparison method")

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.subheader("Additions")
#             st.write(additions)

#         with col2:
#             st.subheader("Subtractions")
#             st.write(subtractions)

#         with col3:
#             st.subheader("Potential Modifications")
#             st.write(potential_modifications)

#         def highlight_text_in_pdf(pdf_path, highlights, color):
#             doc = fitz.open(pdf_path)
#             for page_num in range(len(doc)):
#                 page = doc.load_page(page_num)
#                 for highlight in highlights:
#                     text_instances = page.search_for(highlight)
#                     for inst in text_instances:
#                         highlight = page.add_highlight_annot(inst)
#                         highlight.set_colors(stroke=color)
#                         highlight.update()
#             output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
#             doc.save(output_path)
#             return output_path

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
#             tmp1.write(uploaded_file1.read())
#             tmp1_path = tmp1.name

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
#             tmp2.write(uploaded_file2.read())
#             tmp2_path = tmp2.name

#         highlighted_path1 = highlight_text_in_pdf(tmp1_path, additions, (0, 1, 0))
#         highlighted_path1 = highlight_text_in_pdf(highlighted_path1, subtractions, (1, 1, 0))
#         highlighted_path1 = highlight_text_in_pdf(highlighted_path1, potential_modifications, (1, 0, 0))

#         highlighted_path2 = highlight_text_in_pdf(tmp2_path, additions, (0, 1, 0))
#         highlighted_path2 = highlight_text_in_pdf(highlighted_path2, subtractions, (1, 1, 0))
#         highlighted_path2 = highlight_text_in_pdf(highlighted_path2, potential_modifications, (1, 0, 0))

#         st.subheader("Highlighted PDFs")

#         with open(highlighted_path1, "rb") as file:
#             btn = st.download_button(
#                 label="Download Highlighted Contract 1",
#                 data=file,
#                 file_name="contract1_highlighted.pdf",
#                 mime="application/octet-stream"
#             )

#         with open(highlighted_path2, "rb") as file:
#             btn = st.download_button(
#                 label="Download Highlighted Contract 2",
#                 data=file,
#                 file_name="contract2_highlighted.pdf",
#                 mime="application/octet-stream"


#             )

#     else:
#         st.error("Please upload both PDF files")

highlight_pdf = st.button("Highlight Deviations")


if highlight_pdf:
    
    def highlight_text_in_pdf(pdf_path, highlights, color):
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            for highlight in highlights:
                text_instances = page.search_for(highlight)
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=color)
                    highlight.update()
        output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
        doc.save(output_path)
        return output_path

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
        tmp1.write(uploaded_file1.read())
        tmp1_path = tmp1.name
        
    highlighted_path1 = highlight_text_in_pdf(tmp1_path, ["Please DO NOT ACCESS OR USE the Service, or any Materials that Intel may provide in association with the Service, unless and until you have read, understand"], (0, 1, 0))
    # highlighted_path1 = highlight_text_in_pdf(highlighted_path1, subtractions, (1, 1, 0))
    # highlighted_path1 = highlight_text_in_pdf(highlighted_path1, potential_modifications, (1, 0, 0))


    st.subheader("Highlighted PDFs")

    with open(highlighted_path1, "rb") as file:
        btn = st.download_button(
            label="Download Highlighted Contract 1",
            data=file,
            file_name="contract1_highlighted.pdf",
            mime="application/octet-stream"
        )
        

# updated code to render pdf in frontend instead of download button
# ! need to test it out

# # Set custom CSS for styling
# st.markdown("""
#     <style>
#     .stApp {
#         background-color: #f3f4f6;
#     }
#     .stButton>button {
#         background-color: #0071c5;
#         color: white;
#         border: none;
#         padding: 10px 20px;
#         font-size: 16px;
#         border-radius: 5px;
#     }
#     .stButton>button:hover {
#         background-color: #005aa7;
#         color: white;
#     }
#     .scroll-container {
#         display: flex;
#         overflow-x: scroll;
#     }
#     .scroll-item {
#         flex: 0 0 auto;
#         margin-right: 20px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("Contract Deviation Detection")

# uploaded_file1 = st.file_uploader("Choose the first PDF file", type="pdf")
# uploaded_file2 = st.file_uploader("Choose the second PDF file", type="pdf")

# comparison_method = st.selectbox("Select comparison method", ["jaccard", "levenshtein", "bert"])

# analyze_button = st.button("Analyze Contracts")

# if analyze_button:
#     if uploaded_file1 is not None and uploaded_file2 is not None:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
#             tmp1.write(uploaded_file1.read())
#             tmp1_path = tmp1.name
       
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
#             tmp2.write(uploaded_file2.read())
#             tmp2_path = tmp2.name

#         contract_text1 = extract_text_from_pdf(tmp1_path)
#         contract_text2 = extract_text_from_pdf(tmp2_path)

#         predictions1 = run_prediction(questions, contract_text1, model, tokenizer, device)
#         predictions2 = run_prediction(questions, contract_text2, model, tokenizer, device)

#         col1, col2 = st.columns(2)

#         with col1:
#             st.subheader("Predictions for Contract 1")
#             for question, answer in predictions1.items():
#                 st.write(f"Question: {question}")
#                 st.write(f"Answer: {answer}")
#                 st.write("")

#         with col2:
#             st.subheader("Predictions for Contract 2")
#             for question, answer in predictions2.items():
#                 st.write(f"Question: {question}")
#                 st.write(f"Answer: {answer}")
#                 st.write("")

#     else:
#         st.error("Please upload both PDF files")

# detect_button = st.button("Detect Deviations")

# if detect_button:
#     if uploaded_file1 is not None and uploaded_file2 is not None:
#         if comparison_method == "jaccard":
#             additions, subtractions, potential_modifications = categorize_predictions(predictions1, predictions2)
#         elif comparison_method == "levenshtein":
#             additions, subtractions, potential_modifications = categorize_predictions_levenshetin(predictions1, predictions2)
#         elif comparison_method == "bert":
#             additions, subtractions, potential_modifications = categorize_predictions_with_embeddings(predictions1, predictions2)
#         else:
#             st.error("Invalid comparison method")

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.subheader("Additions")
#             st.write(additions)

#         with col2:
#             st.subheader("Subtractions")
#             st.write(subtractions)

#         with col3:
#             st.subheader("Potential Modifications")
#             st.write(potential_modifications)

#         def highlight_text_in_pdf(pdf_path, highlights, color):
#             doc = fitz.open(pdf_path)
#             for page_num in range(len(doc)):
#                 page = doc.load_page(page_num)
#                 for highlight in highlights:
#                     text_instances = page.search_for(highlight)
#                     for inst in text_instances:
#                         highlight = page.add_highlight_annot(inst)
#                         highlight.set_colors(stroke=color)
#                         highlight.update()
#             output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
#             doc.save(output_path)
#             return output_path

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
#             tmp1.write(uploaded_file1.read())
#             tmp1_path = tmp1.name

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
#             tmp2.write(uploaded_file2.read())
#             tmp2_path = tmp2.name

#         highlighted_path1 = highlight_text_in_pdf(tmp1_path, additions, (0, 1, 0))
#         highlighted_path1 = highlight_text_in_pdf(highlighted_path1, subtractions, (1, 1, 0))
#         highlighted_path1 = highlight_text_in_pdf(highlighted_path1, potential_modifications, (1, 0, 0))

#         highlighted_path2 = highlight_text_in_pdf(tmp2_path, additions, (0, 1, 0))
#         highlighted_path2 = highlight_text_in_pdf(highlighted_path2, subtractions, (1, 1, 0))
#         highlighted_path2 = highlight_text_in_pdf(highlighted_path2, potential_modifications, (1, 0, 0))

#         st.subheader("Highlighted PDFs")

#         # Display PDF 1
#         with open(highlighted_path1, "rb") as file:
#             pdf_bytes = file.read()
#             st.download_button(
#                 label="Download Highlighted Contract 1",
#                 data=pdf_bytes,
#                 file_name="contract1_highlighted.pdf",
#                 mime="application/octet-stream"
#             )
#             st.subheader("Preview of Highlighted Contract 1")
#             st.write("If the PDF preview does not load, please download the file.")
#             st.pdf(pdf_bytes)

#         # Display PDF 2
#         with open(highlighted_path2, "rb") as file:
#             pdf_bytes = file.read()
#             st.download_button(
#                 label="Download Highlighted Contract 2",
#                 data=pdf_bytes,
#                 file_name="contract2_highlighted.pdf",
#                 mime="application/octet-stream"
#             )
#             st.subheader("Preview of Highlighted Contract 2")
#             st.write("If the PDF preview does not load, please download the file.")
#             st.pdf(pdf_bytes)

#     else:
#         st.error("Please upload both PDF files")