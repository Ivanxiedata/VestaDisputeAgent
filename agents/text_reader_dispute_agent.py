import os
import getpass
from dotenv import load_dotenv
import chainlit as cl
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

# Initialize the chat model using Groq provider.
model = init_chat_model("llama3-8b-8192", model_provider="groq")

# Define a system message that instructs the chatbot to act as an AI dispute center staff member.
SYSTEM_PROMPT = (
    "You are an AI dispute center staff member. Your role is to help users resolve disputes by "
    "listening carefully, clarifying issues, summarizing provided details, and offering recommendations. "
    "Always respond in a professional and empathetic tone."
)

@cl.on_chat_start
async def on_chat_start():
    welcome_text = (
        "Welcome to the AI Dispute Center!\n\n"
        "Please describe your dispute in detail and I'll help you resolve it. "
        "For example, you might say, \"I want to dispute a refund because I am a seller and my product arrived on time according to UPS tracking.\""
    )
    await cl.Message(content=welcome_text).send()


@cl.on_message
async def text_reader_main(message: cl.Message):
    # User's input is provided as a HumanMessage.
    human_input = HumanMessage(content=message.content)

    # Build the conversation with a system message and the current human message.
    # (You can also expand this to accumulate a full conversation history if desired.)
    conversation = [
        SystemMessage(content=SYSTEM_PROMPT),
        human_input
    ]

    # Invoke the model with the conversation.
    result = model.invoke(conversation)
    response = result.content


    # Print out the model's response as an AI message.
    # Here result is expected to be a string containing the response.
    await cl.Message(content=response).send()
