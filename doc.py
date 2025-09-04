import streamlit as st
import pandas as pd
import os

def main():
    # -----------------------------
    # Doctor login credentials
    # -----------------------------
    DOCTORS = {
        "dr_smith": "password123",
        "dr_john": "secure456"
    }

    # -----------------------------
    # Files to store pending and resolved cases
    # -----------------------------
    PENDING_FILE = "pending_cases.csv"
    RESOLVED_FILE = "resolved_cases.csv"

    # -----------------------------
    # Helper Functions
    # -----------------------------
    def load_pending_cases():
        if os.path.exists(PENDING_FILE):
            return pd.read_csv(PENDING_FILE)
        else:
            return pd.DataFrame(columns=["case_id", "extracted_text", "ai_analysis", "alerts"])

    def save_resolved_case(case, doctor, decision, comments):
        resolved = pd.DataFrame([{
            "case_id": case["case_id"],
            "extracted_text": case["extracted_text"],
            "ai_analysis": case["ai_analysis"],
            "alerts": case["alerts"],
            "reviewed_by": doctor,
            "decision": decision,
            "comments": comments
        }])
        if os.path.exists(RESOLVED_FILE):
            resolved.to_csv(RESOLVED_FILE, mode='a', header=False, index=False)
        else:
            resolved.to_csv(RESOLVED_FILE, index=False)

    def remove_case_from_pending(case_id):
        if os.path.exists(PENDING_FILE):
            df = pd.read_csv(PENDING_FILE)
            df = df[df["case_id"] != case_id]
            df.to_csv(PENDING_FILE, index=False)

    # -----------------------------
    # Streamlit UI
    # -----------------------------
    st.title("🩺 Doctor Review Panel")

    # Login section
    st.subheader("Doctor Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

if __name__ == "__main__":
    main()