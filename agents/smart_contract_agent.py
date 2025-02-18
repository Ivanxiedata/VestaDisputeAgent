import streamlit as st
from fpdf import FPDF
import datetime
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


# Initialize AI Model (DeepSeek)
LANGUAGE_MODEL = OllamaLLM(model="deepseek-r1:1.5b")

# General Contract Prompt
PROMPT_TEMPLATE = """
You are an expert contract generator. Based on the buyer's and seller's inputs, generate a clear and professional smart contract.

Buyer: {buyer_input}
Seller: {seller_input}

Ensure the contract includes key terms for product conditions, quantity, payment release, shipping conditions, and refund policies.
If additional terms are provided, include them appropriately in the contract.

Contract:
"""


# Function to generate contract using AI
def generate_contract(buyer_input, seller_input, additional_terms=""):
    conversation_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = conversation_prompt | LANGUAGE_MODEL
    contract_text = response_chain.invoke(
        {
            "buyer_input": buyer_input,
            "seller_input": seller_input,
            "additional_terms": additional_terms,
        }
    )
    return contract_text


# Function to generate a PDF






def generate_pdf(contract_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Use built-in font (no external font needed)
    pdf.set_font("Arial", size=12)

    # Encode text as UTF-8 (removing unsupported characters)
    contract_text = contract_text.encode('latin-1', 'ignore').decode('latin-1')

    for line in contract_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf_output = "Smart_Contract.pdf"
    pdf.output(pdf_output, "F")
    return pdf_output


# Streamlit UI
st.title("📜 AI-Powered Smart Contract Generator")
st.markdown("### Buyer and Seller provide prompts, AI generates a contract, and updates it dynamically.")

# User Inputs
buyer_input = st.text_area("Buyer: Describe your contract needs")
seller_input = st.text_area("Seller: Describe your contract needs")

# AI-Suggested Key Terms
st.markdown("### Suggested Keywords for Different Use Cases:")
suggested_keywords = {
    "E-commerce": ["Product condition", "Shipping date", "Return policy", "Payment upon delivery"],
    "Real Estate": ["Lease term", "Deposit amount", "Maintenance responsibility", "Early termination"],
    "Freelance Work": ["Project deadline", "Payment milestones", "Scope of work", "Revisions policy"],
}
selected_category = st.selectbox("Select your contract type:", list(suggested_keywords.keys()))
selected_keywords = st.multiselect("Select keywords to include:", suggested_keywords[selected_category])

# Additional Terms Input
additional_terms = st.text_area("Additional Terms & Conditions (optional)")

# Generate Contract Button
if st.button("Generate Smart Contract"):
    if buyer_input and seller_input:
        combined_terms = f"{', '.join(selected_keywords)}. {additional_terms}"
        contract_text = generate_contract(buyer_input, seller_input, combined_terms)
        st.session_state["contract_text"] = contract_text  # Store contract in session state
        st.success("Smart contract generated successfully!")
        st.text_area("Contract Preview", contract_text, height=300)

        # Provide option to download the contract as PDF
        pdf_path = generate_pdf(contract_text)
        st.download_button(label="Download Contract PDF", data=open(pdf_path, "rb"), file_name="Smart_Contract.pdf",
                           mime="application/pdf")
    else:
        st.error("Both Buyer and Seller inputs are required!")

# Allow User to Modify Contract
st.markdown("---")
st.markdown("### Modify Contract Terms")
if "contract_text" in st.session_state:
    updated_contract_text = st.text_area("Modify the contract if needed:", st.session_state["contract_text"],
                                         height=300)

    if st.button("Update Contract"):
        st.session_state["contract_text"] = updated_contract_text
        pdf_path = generate_pdf(updated_contract_text)
        st.success("Contract updated successfully!")
        st.download_button(label="Download Updated Contract PDF", data=open(pdf_path, "rb"),
                           file_name="Updated_Smart_Contract.pdf", mime="application/pdf")
