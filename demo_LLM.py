import getpass
import os
from dotenv import main

# prepare the environment
main.load_dotenv()
os.environ["MISTRAL_API_KEY"]=os.getenv("MISTRAL_API_KEY")

# initialize the model
from langchain.chat_models import init_chat_model
model = init_chat_model("mistral-small-latest", model_provider="mistralai")
# here we can choose other mistral AI's model:
# https://docs.mistral.ai/getting-started/models/models_overview/

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

with open('mountain.txt') as f:
    mountain = f.read()
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
chunk_size = 100, #number of characters for each chunk
chunk_overlap = 20,#number of characters overlapping between a preceding and following chunk
length_function = len #function used to measure the number of characters
)
texts = text_splitter.create_documents([mountain])


from langchain_mistralai import MistralAIEmbeddings
# Setting which embedding model you want to use.
embeddings_model = MistralAIEmbeddings(model="mistral-embed")
embeddings = embeddings_model.embed_documents(
[ # You can also use Chinese to test your code
"Good morning!",
"Oh, hello!",
"I want to report an accident",
"Sorry to hear that. May I ask your name?",
"Sure, Mario Rossi."
]
)

# Take 紅樓夢 as an example, you have used it on the previous part
raw_documents = TextLoader('dreamOftheRedChamber.txt',encoding='utf-8').load()
# the text_splitter you have built on the previous part
documents = text_splitter.split_documents(raw_documents)
# build the vector store and here we use FAISE
db = FAISS.from_documents(documents,embeddings_model)
from langchain.chains import RetrievalQA
retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever)

from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
memory = ConversationSummaryMemory(llm=model)
memory.save_context({"input": "hi, I'm looking for some ideas to write an essay in AI"},
{"output": "hello, what about writing on LLMs?"})

from langchain.agents import AgentType, initialize_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import BaseTool, StructuredTool, Tool, tool

search = DuckDuckGoSearchRun()
tools = [Tool.from_function(
func=search.run,
name="Search",
description="useful for when you need to answer questions about current events"
)]
agent = initialize_agent(tools, llm = model, # USE YOUR LLM MODEL HERE
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("大谷翔平是哪一隊？")