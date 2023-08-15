import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
import pinecone
import PyPDF2


# Constants for text chunk size and overlap
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 150


def process_text_file(text_file_path):
    # API keys
    OPENAI_API_KEY = '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'
    PINECONE_API_KEY = '7fa9a358-54ff-477b-b88f-3120f7c506ca'
    PINECONE_ENV = 'northamerica-northeast1-gcp'

    # Load the text file and split it into smaller chunks
    loader = TextLoader(text_file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=150
    )
    docs = text_splitter.split_documents(documents)

    # Create an instance of the OpenAIEmbeddings class
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002',
        openai_api_key=OPENAI_API_KEY
    )

    # Initialize Pinecone and create an index
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV
    )
    index_name = "rivvi-pdfs"
    docsearch = Pinecone.from_documents(
        docs,
        embeddings,
        index_name=index_name
    )

    # Perform similarity search on the index
    query = "What is this document about?"
    docs = docsearch.similarity_search(query)

    # Print the content of the most similar document
    # print(docs[0].page_content)

    # Error handling for file upload
    try:
        # Code for creating embeddings and storing them in Pinecone
        print("File upload successful")
        return True
    except Exception as e:
        print("File upload failed:", str(e))
        return False


def convert_pdf_to_text(pdf_path, output_text_files):
    global CHUNK_SIZE, CHUNK_OVERLAP  # Specify that we are using the global variables

    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

        # Ensure the chunk size is not larger than the actual text length
        if len(text) < CHUNK_SIZE:
            CHUNK_SIZE = len(text)

        # Split the text into smaller chunks
        text_chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP)]

        # Create the output text files and store the text chunks
        for i, chunk in enumerate(text_chunks):
            output_text_file = f"{pdf_path}_{i}.txt"
            with open(output_text_file, "w", encoding="utf-8") as output_file:
                output_file.write(chunk)
            output_text_files.append(output_text_file)

        print("PDF converted to text files successfully.")
        return output_text_files
    except Exception as e:
        print("Error converting PDF to text:", str(e))
        return []



# Rest of the code remains unchanged...

def process_all_files_in_uploader():
    # Get a list of all files in the "uploader" directory
    uploader_directory = "./uploader"
    files = [file for file in os.listdir(uploader_directory) if file.lower().endswith('.pdf')]

    for file in files:
        pdf_path = os.path.join(uploader_directory, file)
        print(f"Processing file: {file}")

        # Convert the PDF to text
        output_text_files = convert_pdf_to_text(pdf_path, [])

        if output_text_files:
            for output_text_file in output_text_files:
                # Add a check to see if the text file exists before processing it
                if os.path.exists(output_text_file):
                    process_text_file(output_text_file)
                    os.remove(output_text_file)
                else:
                    print(f"Error: Text file '{output_text_file}' not found.")


# Call the function to process all files in the "uploader" directory
process_all_files_in_uploader()
