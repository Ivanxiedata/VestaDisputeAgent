import re
import chainlit as cl
from fpdf import FPDF
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize the language model (DeepSeek)
LANGUAGE_MODEL = OllamaLLM(model="deepseek-r1:1.5b")

# General Contract Prompt Template
PROMPT_TEMPLATE = """
You are an expert contract generator. Based on the buyer's and seller's inputs, generate a clear and professional smart contract.

Buyer: {buyer_input}
Seller: {seller_input}

Ensure the contract includes key terms for product conditions, quantity, payment release, shipping conditions, and refund policies.
If additional terms are provided, include them appropriately in the contract.

Contract:
"""

# Define suggested keywords for each contract type.
SUGGESTED_KEYWORDS = {
    "E-commerce": ["Product condition", "Shipping date", "Return policy", "Payment upon delivery"],
    "Real Estate": ["Lease term", "Deposit amount", "Maintenance responsibility", "Early termination"],
    "Freelance Work": ["Project deadline", "Payment milestones", "Scope of work", "Revisions policy"],
}

# ----- Functions from your original code -----
def generate_contract(buyer_input, seller_input, additional_terms=""):
    conversation_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = conversation_prompt | LANGUAGE_MODEL
    contract_text = response_chain.invoke({
        "buyer_input": buyer_input,
        "seller_input": seller_input,
        "additional_terms": additional_terms,
    })
    # Clean the output to remove any chain-of-thought tags and content
    contract_text = clean_contract_output(contract_text)
    return contract_text

def generate_pdf(contract_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Remove unsupported characters by encoding/decoding with latin-1
    contract_text = contract_text.encode('latin-1', 'ignore').decode('latin-1')
    for line in contract_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_output = "Smart_Contract.pdf"
    pdf.output(pdf_output, "F")
    return pdf_output

def clean_contract_output(text: str) -> str:
    """
    Removes any content enclosed in <think> ... </think> including the tags.
    """
    # The DOTALL flag ensures that the dot matches newline characters.
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned_text.strip()

# ----- Conversation State Management -----
conversation_state = {
    "step": "greeting",   # conversation step marker
    "buyer_input": "",
    "seller_input": "",
    "contract_type": "",
    "selected_keywords": [],
    "additional_terms": "",
    "contract_text": ""
}

# ----- Chainlit Event Handlers -----
@cl.on_chat_start
async def on_chat_start():
    welcome_text = (
        "Welcome to the AI-Powered Smart Contract Generator!\n\n"
        "I'll guide you step by step to generate your smart contract.\n"
        "When you are ready, please type **start**."
    )
    await cl.Message(content=welcome_text).send()

@cl.on_message
async def smart_contract_main(message: cl.Message):
    global conversation_state

    # Start conversation
    if conversation_state["step"] == "greeting":
        if message.content.strip().lower() == "start":
            conversation_state["step"] = "buyer_input"
            await cl.Message(content="Please enter the **Buyer** details (e.g., contract requirements):").send()
        else:
            await cl.Message(content="Please type **start** to begin the process.").send()
        return

    # Step 1: Get Buyer Input
    if conversation_state["step"] == "buyer_input":
        conversation_state["buyer_input"] = message.content.strip()
        conversation_state["step"] = "seller_input"
        await cl.Message(content="Great. Now, please enter the **Seller** details (e.g., contract requirements):").send()
        return

    # Step 2: Get Seller Input
    if conversation_state["step"] == "seller_input":
        conversation_state["seller_input"] = message.content.strip()
        conversation_state["step"] = "contract_type"
        contract_types = list(SUGGESTED_KEYWORDS.keys())
        types_str = "\n".join(f"- {ct}" for ct in contract_types)
        await cl.Message(content=f"Please choose a contract type from the following options:\n{types_str}\n\nType the name exactly as shown.").send()
        return

    # Step 3: Get Contract Type
    if conversation_state["step"] == "contract_type":
        ct = message.content.strip()
        if ct not in SUGGESTED_KEYWORDS:
            await cl.Message(content="Invalid contract type. Please enter one of the available options.").send()
            return
        conversation_state["contract_type"] = ct
        conversation_state["step"] = "selected_keywords"
        keywords_list = SUGGESTED_KEYWORDS[ct]
        keywords_str = ", ".join(keywords_list)
        await cl.Message(content=(
            f"For **{ct}** contracts, here are some suggested keywords: {keywords_str}.\n"
            "Please type the keywords you want to include (comma-separated), or type 'none' to skip."
        )).send()
        return

    # Step 4: Get Selected Keywords
    if conversation_state["step"] == "selected_keywords":
        text = message.content.strip()
        if text.lower() == "none":
            conversation_state["selected_keywords"] = []
        else:
            conversation_state["selected_keywords"] = [kw.strip() for kw in text.split(",") if kw.strip()]
        conversation_state["step"] = "additional_terms"
        await cl.Message(content="Please enter any **Additional Terms & Conditions** (or type 'none' to skip):").send()
        return

    # Step 5: Get Additional Terms and Generate Contract
    if conversation_state["step"] == "additional_terms":
        text = message.content.strip()
        conversation_state["additional_terms"] = "" if text.lower() == "none" else text.strip()

        # Combine keywords with additional terms
        keywords_text = ", ".join(conversation_state["selected_keywords"])
        combined_terms = f"{keywords_text}. {conversation_state['additional_terms']}".strip()

        await cl.Message(content="Generating your smart contract, please wait...").send()
        contract_text = generate_contract(
            conversation_state["buyer_input"],
            conversation_state["seller_input"],
            combined_terms
        )
        conversation_state["contract_text"] = contract_text

        # Send the contract preview without the chain-of-thought artifacts
        await cl.Message(content=f"### Generated Smart Contract:\n```\n{contract_text}\n```").send()

        # Generate PDF and send as a file
        pdf_path = generate_pdf(contract_text)
        await cl.File(
            path=pdf_path,
            file_name="Smart_Contract.pdf",
            description="Download your smart contract as a PDF."
        ).send()

        # Offer modification step
        conversation_state["step"] = "modify_contract"
        await cl.Message(content="If you would like to modify the contract, please paste your modified contract text. "
                                   "Otherwise, type 'done' to finish.").send()
        return

    # Step 6: Allow user to modify the contract text
    if conversation_state["step"] == "modify_contract":
        if message.content.strip().lower() == "done":
            await cl.Message(content="Thank you for using the Smart Contract Generator.").send()
            # Optionally, reset the conversation state here.
            conversation_state.clear()
            conversation_state.update({
                "step": "greeting",
                "buyer_input": "",
                "seller_input": "",
                "contract_type": "",
                "selected_keywords": [],
                "additional_terms": "",
                "contract_text": ""
            })
        else:
            conversation_state["contract_text"] = message.content.strip()
            pdf_path = generate_pdf(conversation_state["contract_text"])
            await cl.Message(content="Contract updated successfully! Here is your updated contract preview:").send()
            await cl.Message(content=f"```\n{conversation_state['contract_text']}\n```").send()
            await cl.File(
                path=pdf_path,
                file_name="Updated_Smart_Contract.pdf",
                description="Download your updated smart contract as a PDF."
            ).send()
            await cl.Message(content="If no further modifications are needed, type 'done'.").send()
        return
