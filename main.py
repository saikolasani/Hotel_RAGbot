
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.vectorstores.pgvector import PGVector
#from langchain.embeddings import VertexAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai import VertexAIEmbeddings
import psycopg2
from google.cloud import aiplatform
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
import os
from google.cloud import aiplatform
from langchain_astradb import AstraDBVectorStore
from langchain_google_vertexai import VertexAIEmbeddings

embedding = VertexAIEmbeddings()
vstore = AstraDBVectorStore(
    embedding=embedding,
    collection_name="hotel_embeddings",
    token="AstraCS:uyGjAfTBKJGEkzDRcnQAuved:8f96e3aaa89b517c44931fb815cc8a6a9606ac3a86a10eadf13b223d2f192216",
    api_endpoint="https://d76dcb8a-2c6c-41ad-8000-0849aed20095-us-east1.apps.astra.datastax.com",
)



aiplatform.init(project=f"hackathon-420400", location=f"us-central1")
embeddings_service = VertexAIEmbeddings(model_name="textembedding-gecko")


llm = ChatVertexAI(model_name="gemini-1.0-pro", temperature=0.1, max_output_tokens=300)

verbose = False

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
The standalone question has to be made in first-person from the user point of view.


Beginning of the example 1.
Input:
=========
Chat history:
[{{"human": "Can you recommend a restaurant in Boston?"}}, {{"assistant": "Sure, the restaurant <EXAMPLE> is a good choice."}}]

Follow up question: is there a japanese cuisine option?
=========
Example output:
Can you tell me if the restaurant <EXAMPLE> has a japanese cuisine option?
=========
End of the example 1.

Beginning of the example 2.
Input:
=========
Chat history:
[]

Follow up question: is there a japanese cuisine option?
=========
Example output:
is there a japanese cuisine option?
=========
End of the example 2.



Chat History:
{chat_history}

Follow up question: {question}""")



template = """
You're an assistant called Priceline Penny. You're a chatbot in the Priceline website.
Priceline website offers solution for booking hotels and restaurant world-wide.

Your goal is to help the user to answer questions about the website, hotels, restaurants and reservations.
Don't make politicals, religious or any other assumptions and don't even talk about this, just focus on the Priceline offer.
Use the same language of the input question.


If there's no answer for the user, say "I don't know, please contact the support".
If the user is asking to policies, only use information provided in this prompt. Do not make up rules.

When suggesting an hotel or restaurant, include the name, the area, the address and explain why it's a good choice.
Do not make up any data about them, only use details provided in this instruction.

When the user asks about hotels, provide a list of available hotels with their names, locations, description in a bulleted format. Omit additional information like "Other factors to consider" and avoid asking clarifying questions or making suggestions.


The following list are hotels/restaurant in HTML format. Use these items only if you need to search an hotel or restaurant. This list is not exhaustive but only contains relevant content.
<context>
{context}
</context>

This is the chat history:
<chat-history>
{chat_history}
</chat-history>

This is the question that you need to answer (considering the chat history too):
Question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.chat_memory.clear()
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=verbose
)
chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name="context"

)
condense_question_chain = LLMChain(
    llm=llm,
    prompt=CONDENSE_QUESTION_PROMPT,
    verbose=verbose
)

def format_history(chat_history):
  all = []


  for dialogue_turn in chat_history:
    if dialogue_turn.type == "human":
      prefix = "Human"
    else:
      prefix = "Assistant (you)"
    all.append({"role": prefix, "content": dialogue_turn.content})

  import json
  return json.dumps(all)



conversation = ConversationalRetrievalChain(
    combine_docs_chain=chain,
    retriever=vstore.as_retriever(search_kwargs={"k": 3}),
    question_generator=condense_question_chain,
    memory=memory,
    get_chat_history=format_history
)



while True:
  q = input("\nYou: ")
  answer = conversation.invoke({"question": q})
  print("\nhotel_ragbot: ", answer["answer"])



