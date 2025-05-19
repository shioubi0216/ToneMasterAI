import os
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
import logging

class AIService:
    def __init__(self):
        """Initialize the AI service with Mistral AI models"""
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            logging.warning("MISTRAL_API_KEY not found in environment variables")
            
        try:
            self.llm = ChatMistralAI(
                model="mistral-small-latest", 
                mistral_api_key=self.api_key
            )
            self.embeddings = MistralAIEmbeddings(
                model="mistral-embed",
                mistral_api_key=self.api_key
            )
            logging.info("AI Service initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing AI Service: {e}")
            raise
            
    def generate_example_sentences(self, character, interests=None):
        """Generate example sentences using the character based on user interests"""
        interests_text = ", ".join(interests) if interests else "general topics"
        
        prompt = PromptTemplate(
            input_variables=["character", "interests"],
            template="""
            Create 3 simple example Japanese sentences that use the Japanese character '{character}'. 
            Make the sentences related to {interests} if possible.
            For each sentence provide:
            1. The Japanese sentence
            2. Romaji pronunciation
            3. English translation
            
            Format each example as:
            Japanese: [Japanese sentence]
            Romaji: [Romaji]
            English: [English translation]
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(character=character, interests=interests_text)
        return response
        
    def get_learning_tips(self, character):
        """Generate tips for memorizing the given character"""
        prompt = PromptTemplate(
            input_variables=["character"],
            template="""
            Provide 2-3 helpful tips for remembering and writing the Japanese character '{character}'.
            Include any mnemonics, visual similarities, or common confusions to watch out for.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(character=character)
        return response
        
    def create_personalized_learning_path(self, interests):
        """Create a personalized learning path based on user interests"""
        interests_text = ", ".join(interests)
        
        prompt = PromptTemplate(
            input_variables=["interests"],
            template="""
            Create a personalized Japanese syllabary learning path for a beginner who is interested in: {interests}.
            
            The learning path should include:
            1. A recommended order for learning hiragana and katakana characters
            2. 5 themed vocabulary groups related to their interests (with 3-4 example words each)
            3. A suggested 2-week schedule with specific goals
            
            Make the learning path engaging and connected to the person's interests.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(interests=interests_text)
        return response
