
from tools.PDFTextExtractor import PDFTextExtractor
from tools.PDFOCRExtractor import PDFOCRExtractor
import os 
from dotenv import load_dotenv

load_dotenv()
class tools: 
    def __init__(self): 

        # This is for the connection string for the database -> The only connection string that is needed to
        # Connect to CoackRaochDB
        self.db_connection = os.getenv("DATABASE_URL")

        # Creating the instances of both the retrival and insert tools
        self.PDFTextExtractor = PDFTextExtractor()
        self.PDFOCRExtractor = PDFOCRExtractor()
        # Building the services that will be used to invoke the tools itslef

        self.PDFTextExtractorService = self.PDFTextExtractor.run
        self.PDFOCRExtractorService = self.PDFOCRExtractor.run

        self.tools_list = [self.PDFTextExtractorService, self.PDFOCRExtractorService] 

    def toolkit(self): 
        return self.tools_list
    
# if __name__ == "__main__":
#     tools_instance = tools()
#     li = tools_instance.toolkit()

#     # Correct usage
#     result = li[1]("./testing.pdf")  # Only this line is needed
#     print(result)