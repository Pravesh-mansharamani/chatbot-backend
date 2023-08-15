import os
import PyPDF2
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader


def convert_pdf_to_text(pdf_file_path):
    try:
        with open(pdf_file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

        output_text_file = os.path.splitext(pdf_file_path)[0] + ".txt"
        with open(output_text_file, "w", encoding="utf-8") as output_file:
            output_file.write(text)

        print(f"PDF converted to text: {pdf_file_path}")
        return output_text_file
    except Exception as e:
        print(f"Error converting PDF to text: {pdf_file_path}", str(e))
        return None


def process_text_file(text_file_path):
    # API keys
    OPENAI_API_KEY = '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'
    PINECONE_API_KEY = '7fa9a358-54ff-477b-b88f-3120f7c506ca'
    PINECONE_ENV = 'northamerica-northeast1-gcp'

    # Load the text file and split it into smaller chunks
    loader = TextLoader(text_file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50
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
    query = "What are the skills mentioned"
    docs = docsearch.similarity_search(query)

    # Print the content of the most similar document
    print(docs[0].page_content)

    # Error handling for file upload
    try:
        # Code for creating embeddings and storing them in Pinecone
        print("File upload successful")
        return True
    except Exception as e:
        print("File upload failed:", str(e))
        return False


def process_pdf_file(pdf_file_path):
    print(f"Processing PDF: {pdf_file_path}")

    # Convert PDF to text
    text_file_path = convert_pdf_to_text(pdf_file_path)
    if text_file_path is None:
        return False

    # Process the text file
    result = process_text_file(text_file_path)
    if result:
        # Remove the PDF and text files after successful processing
        os.remove(pdf_file_path)
        # os.remove(text_file_path)
        print(f"PDF and text files removed: {pdf_file_path}, {text_file_path}")
    else:
        print("Processing failed. Files not removed.")

    return result


def process_all_pdf_files(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Check if the file has a PDF extension
        if filename.lower().endswith('.pdf'):
            # Construct the full path to the PDF file
            file_path = os.path.join(directory, filename)

            # Process the PDF file
            process_pdf_file(file_path)


def process_pdfs_in_directory(directory):
    # Process PDF files in the directory
    process_all_pdf_files(directory)


# Call the function to process PDF files in the uploader directory
pdf_directory = './uploader'
process_pdfs_in_directory(pdf_directory)
