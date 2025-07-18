
import time
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import sys 
import os
from langchain_mistralai import ChatMistralAI
import time
import dotenv
dotenv.load_dotenv()
# Having a system path so that the files are all readable
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from tools.utility import tools
from utils.utils import AgentState

class Agent(): 
    def __init__(self):
        self.mistral_model = ChatMistralAI(model="mistral-large-latest", temperature=0, api_key=os.getenv("MISTRAL_API_KEY"))

    
        Tool = tools()
        self.tools = Tool.toolkit()

        
        self.model_with_tool = self.mistral_model.bind_tools(self.tools)
    def system_prompt(self) -> SystemMessage:
        """Text extraction expert ."""
        return SystemMessage(
            content=( """

                 You will be given a PDF document containing unstructured data or a URL pointing to the file location.
            Imagine three highly intelligent agents who are experts in document extraction and analysis.
            They are capable of reading and understanding complex documents, extracting key information, and providing structured outputs.
            They can handle unstructured data and convert it into structured formats such as JSON or triplets.

            These agents have access to the following tools:

            extract_text_from_pdf: This tool extracts text from PDF documents, including those with complex layouts or embedded images. And will use tesseract_ocr_from_pdf as a fallback when standard text extraction is insufficient.
            tesseract_ocr_from_pdf: This tool performs OCR on pages with mixed content (e.g., scanned images, photographs, or handwriting) and serves as a fallback when standard text extraction is insufficient.

            The agents will collaborate to ensure the best results. They will:

            Rank every meaningful piece of information based on relevance and importance.

            Clean and structure the extracted data.

            Preserve key metadata, such as page numbers, for accurate source citation.

            """
            )
        )

    def run_agent(self, state: AgentState, config: RunnableConfig) -> dict:
        time.sleep(3)

        response = self.model_with_tool.invoke([self.system_prompt()] + state["messages"], config)

        
        return {"messages": [response]}

