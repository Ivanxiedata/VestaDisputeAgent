import os
import PyPDF2
from PIL import Image
import pytesseract
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS  # using FAISS as our in-memory vector store
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import chainlit as cl
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize GROQ language model
groq_api_key = os.environ['GROQ_API_KEY']
llm_groq = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192",
    temperature=0.2
)


def extract_text_from_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    pdf = PyPDF2.PdfReader(path)
    pdf_text = ""
    for page in pdf.pages:
        pdf_text += page.extract_text() or ""
    return pdf_text


def extract_text_from_image(path: str) -> str:
    """Extract text from an image file using OCR."""
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return text


@cl.on_chat_start
async def on_chat_start():
    files = None

    # Accept both PDF and image files.
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload one or more PDF or image files to begin!",
            accept=["application/pdf", "image/*"],
            max_size_mb=100,
            max_files=10,
            timeout=180,
        ).send()

    texts = []
    metadatas = []
    for file in files:
        # Determine the file type based on the extension or content type.
        file_ext = os.path.splitext(file.name)[1].lower()

        if file_ext in [".pdf"]:
            extracted_text = extract_text_from_pdf(file.path)
        elif file_ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            extracted_text = extract_text_from_image(file.path)
        else:
            # Skip unsupported file types
            extracted_text = ""

        # Only continue if text was extracted
        if extracted_text:
            # Split the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=50)
            file_texts = text_splitter.split_text(extracted_text)
            texts.extend(file_texts)

            # Create metadata for each chunk
            file_metadatas = [{"source": f"{i}-{file.name}"} for i in range(len(file_texts))]
            metadatas.extend(file_metadatas)

    if not texts:
        await cl.Message(content="No text could be extracted from the uploaded files.").send()
        return

    # Initialize the embedding model
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")

    # Create an in-memory FAISS vector store
    docsearch = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)

    # Set up conversation memory and chain
    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm_groq,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Optionally, send an image to indicate processing is complete.
    elements = [cl.Image(name="image", display="inline", path="image_store/VestaLogo.png")]
    msg = cl.Message(content=f"Processing {len(files)} files done. You can now ask questions!", elements=elements)
    await msg.send()

    # Store the chain in the user session
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.ainvoke(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]

    text_elements = []
    # Uncomment below if you want to show source document snippets:
    # if source_documents:
    #     for source_idx, source_doc in enumerate(source_documents):
    #         source_name = f"source_{source_idx}"
    #         text_elements.append(cl.Text(content=source_doc.page_content, name=source_name))
    #     source_names = [text_el.name for text_el in text_elements]
    #     if source_names:
    #         answer += f"\nSources: {', '.join(source_names)}"
    #     else:
    #         answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()
