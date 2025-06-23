from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from pathlib import Path
import pdfplumber
from crewai_tools import BaseTool
from typing import Any, Optional, Type

class FixedFileReadToolSchema(BaseModel):
    """Input for FileReadTool."""

    pass


class FileReadToolSchema(FixedFileReadToolSchema):
    """Input for FileReadTool."""

    pdf_file_path: str = Field(..., description="Mandatory file full path to read the file")

class PDFReaderTool(BaseTool):
    name: str = "Read a file's content"
    description: str = "A tool that can be used to read a file's content."
    pdf_file_path: Optional[str] = None
    
    def __init__(self, pdf_file_path: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if pdf_file_path is not None:
            self.pdf_file_path = pdf_file_path
            self.description = f"A tool that can be used to read {pdf_file_path}'s content."
            self.args_schema = FixedFileReadToolSchema
            self._generate_description()
            
    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        try:
            pdf_file_path = kwargs.get("pdf_file_path", self.pdf_file_path)
            print(f"Attempting to read file: {pdf_file_path}")  # Log
            with pdfplumber.open(pdf_file_path, 'r') as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                print(f"Successfully read {len(pdf.pages)} pages")  # Log
                return text if text else "O PDF não contém texto."
        except Exception as e:
            print(f"Error reading file: {e}")  # Log
            return f"Fail to read the file {pdf_file_path}. Error: {e}"


# Exemplo de uso da ferramenta
caminho_arquivo = Path(__file__).parents[0] / 'artigos' / 'AUTOMATIC-CHAIN-OF-THOUGHT-PROMPTING-IN-LARGE-LANGUAGE-MODELS.pdf'
pdf_tool = PDFReaderTool(str(caminho_arquivo))

class Artigo(BaseModel):
    """Modelo de quebra do artigo"""
    titulo: str = Field(..., description="Título do item")
    texto: str = Field(..., description="Texto do item")
    


@CrewBase
class TradutoraArtigo():
    """    
    """

    def __init__(self, llm, max_rpm) -> None:
        """             
        """

        self.llm = llm
        self.max_rpm = max_rpm 

    @agent
    def leitor_pdf(self) -> Agent:
        """        
        """        
        return Agent(
            config=self.agents_config['leitor_pdf'],
            llm=self.llm,
            max_rpm=self.max_rpm,
            memory=True,
            allow_delegation=False,
            verbose=True,            
        )    
   
    @task
    def tarefa_analise_texto(self) -> Task: 
        """        
        """
        return Task(
            config=self.tasks_config['tarefa_leitor_pdf'],
            agent=self.leitor_pdf(),
            tools=[pdf_tool],
            output_json=Artigo
        )
    
    
    

    @crew
    def crew(self) -> Crew:
        """        
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            cache=True,
            verbose=True,			
        )