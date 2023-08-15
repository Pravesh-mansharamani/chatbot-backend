import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains import RetrievalQAWithSourcesChain


def query_answer(query):
    # OPEN AI API KEYS
    OPENAI_API_KEY = "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"
    model_name = 'text-embedding-ada-002'

    embed = OpenAIEmbeddings(
        model=model_name,
        openai_api_key=OPENAI_API_KEY
    )

    # pinecone API KEYS
    YOUR_API_KEY = "7fa9a358-54ff-477b-b88f-3120f7c506ca"
    YOUR_ENV = "northamerica-northeast1-gcp"
    index_name = 'rivvi-pdfs'

    pinecone.init(
        api_key=YOUR_API_KEY,
        environment=YOUR_ENV
    )

    text_field = "text"

    # switch back to normal index for langchain
    index = pinecone.Index(index_name)

    vectorstore = Pinecone(
        index, embed.embed_query, text_field
    )

    # completion llm
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name='gpt-3.5-turbo',
        temperature=0.2,
    )

    # qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=vectorstore.as_retriever()
    # )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    # print(qa_with_sources(query))
    return qa.run(query)

# print(query_answer("what is the vacation pay in ontario?"))
