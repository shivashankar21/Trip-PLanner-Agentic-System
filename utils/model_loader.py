import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai", "gemini"] = "gemini"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file or environment.")
            model_name = self.config["llm"]["groq"]["model_name"]
            if not model_name:
                raise ValueError("Groq model name is not configured in config.yaml")
            try:
                llm = ChatGroq(model=model_name, api_key=groq_api_key)
            except Exception as e:
                raise ValueError(f"Failed to initialize Groq LLM: {str(e)}")
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file or environment.")
            model_name = self.config["llm"]["openai"]["model_name"]
            if not model_name:
                raise ValueError("OpenAI model name is not configured in config.yaml")
            try:
                llm = ChatOpenAI(model=model_name, api_key=openai_api_key)
            except Exception as e:
                raise ValueError(f"Failed to initialize OpenAI LLM: {str(e)}")
        elif self.model_provider == "gemini":
            print("Loading LLM from Google Gemini..............")
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it in your .env file or environment.")
            model_name = self.config["llm"]["gemini"]["model_name"]
            if not model_name:
                raise ValueError("Gemini model name is not configured in config.yaml")
            try:
                llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=google_api_key)
            except Exception as e:
                raise ValueError(f"Failed to initialize Gemini LLM: {str(e)}")
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
        
        return llm
    