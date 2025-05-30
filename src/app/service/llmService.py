import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI
from service.Expense import Expense

class LLMService:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        print("Loading .env from:", dotenv_path)
        load_dotenv(dotenv_path)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",           
                """
                You are an expert extraction algorithm.
                Only extract relevant information from the text.
                If you do not know the value of an attribute asked to extract,
                return null for the attribute's value.
                in amount only keep the value not the currency
                """
            ),  
            ("human","{text}")
        ])

        self.apiKey = os.getenv('OPENAI_API_KEY')
        self.llm = ChatMistralAI(api_key=self.apiKey,model = "mistral-large-latest")
        self.runnable = self.prompt | self.llm.with_structured_output(schema=Expense)   
    
    def runLLM(self,message):
        return self.runnable.invoke({"text":message})