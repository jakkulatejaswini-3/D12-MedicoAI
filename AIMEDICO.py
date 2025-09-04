# main.py
import streamlit as st
import gradio as gr
from transformers import pipeline
import easyocr
import pandas as pd

# -----------------------------
# Load IBM Granite model
# -----------------------------
pipe = pipeline("text-generation", model="ibm-granite/granite-3.3-2b-instruct")

# -----------------------------
# Load OCR reader
# -----------------------------
reader = easyocr.Reader(['en'])  # English only for simplicity

# -----------------------------
# Sample medical knowledge base
# -----------------------------
# In real scenario, replace with a full drug database
drug_db = pd.DataFrame({
    "drug_name": ["Paracetamol", "Ibuprofen", "Amoxicillin"],
    "dosage_mg": [500, 200, 250]
})

# -----------------------------
# Drug Name Mapping (for Travel)
# -----------------------------
drug_name_map = {
    "Paracetamol": {"India": "Paracetamol", "USA": "Acetaminophen", "UK": "Paracetamol"},
    "Ibuprofen": {"India": "Ibuprofen", "USA": "Ibuprofen", "UK": "Ibuprofen"},
    "Amoxicillin": {"India": "Amoxycillin", "USA": "Amoxicillin", "UK": "Amoxicillin"},
}

def convert_drug_name(drug, country):
    drug = drug.capitalize()
    if drug in drug_name_map:
        return drug_name_map[drug].get(country, "No equivalent found")
    else:
        return "Drug not found in database"

# -----------------------------
# Function to process prescription image
# -----------------------------
def process_prescription(image):
    # OCR to extract text
    result = reader.readtext(image, detail=0)
    prescription_text = " ".join(result)

    # AI Verification using IBM Granite
    prompt = f"Check the following prescription for errors and verify drug names/dosages:\n{prescription_text}"
    ai_response = pipe(prompt, max_new_tokens=200)[0]['generated_text']

    # Cross-check with knowledge base
    alerts = []
    for drug in drug_db['drug_name']:
        if drug.lower() in prescription_text.lower():
            prescribed_dosage = [word for word in prescription_text.split() if word.isdigit()]
            if prescribed_dosage:
                if int(prescribed_dosage[0]) != int(drug_db[drug_db['drug_name']==drug]['dosage_mg'].values[0]):
                    alerts.append(f"Dosage mismatch for {drug}")
    return {
        "extracted_text": prescription_text,
        "ai_analysis": ai_response,
        "alerts": alerts
    }

# -----------------------------
# Streamlit frontend
# -----------------------------
st.title("AI Prescription Verification System")

uploaded_file = st.file_uploader("Upload Prescription (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Prescription", use_column_width=True)
    result = process_prescription(uploaded_file)
    st.subheader("Extracted Prescription Text")
    st.write(result['extracted_text'])
    st.subheader("AI Verification")
    st.write(result['ai_analysis'])
    if result['alerts']:
        st.subheader("Alerts / Warnings")
        for alert in result['alerts']:
            st.warning(alert)

# -----------------------------
# Streamlit Drug Name Converter
# -----------------------------
st.subheader("🌍 Drug Name Converter (for International Travel)")
drug_input = st.text_input("Enter Drug Name (e.g., Paracetamol)")
country_input = st.selectbox("Select Country", ["India", "USA", "UK"])
if st.button("Convert Drug Name"):
    converted_name = convert_drug_name(drug_input, country_input)
    st.success(f"In {country_input}, '{drug_input}' is known as: {converted_name}")

# -----------------------------
# Gradio Interfaces
# -----------------------------
def gradio_interface(image):
    result = process_prescription(image)
    return result["extracted_text"], result["ai_analysis"], "\n".join(result["alerts"]) if result["alerts"] else "No alerts"

def gradio_converter(drug, country):
    return convert_drug_name(drug, country)

with gr.Blocks() as demo:
    with gr.Tab("Prescription Verification"):
        gr.Interface(
            fn=gradio_interface,
            inputs=gr.Image(type="pil"),
            outputs=[
                gr.Textbox(label="Extracted Text"),
                gr.Textbox(label="AI Verification"),
                gr.Textbox(label="Alerts / Warnings")
            ]
        )
    with gr.Tab("Drug Name Converter"):
        gr.Interface(
            fn=gradio_converter,
            inputs=[gr.Textbox(label="Drug Name"), gr.Dropdown(["India", "USA", "UK"], label="Country")],
            outputs=gr.Textbox(label="Equivalent Name")
        )

demo.launch(share=True)