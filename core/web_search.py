import logging
from duckduckgo_search import DDGS
from swarm import Swarm, Agent
import os
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearchAgent:
    """
    Agente per la ricerca web che utilizza OpenAI Swarm e DuckDuckGo Search
    per ottenere informazioni aggiornate su un argomento.
    """
    
    def __init__(self, openai_key=None):
        """
        Inizializza l'agente di ricerca web.
        
        Args:
            openai_key (str, optional): Chiave API di OpenAI. Se non fornita, viene utilizzata
                                        la variabile d'ambiente OPENAI_API_KEY.
        """
        self.openai_key = openai_key if openai_key else os.getenv('OPENAI_API_KEY')
        # Creiamo prima il client OpenAI
        openai_client = OpenAI(api_key=self.openai_key)
        # Poi passiamo il client a Swarm
        self.swarm_client = Swarm(client=openai_client)
        self.ddgs = DDGS()
        
        # Inizializza gli agenti
        self.search_agent = self._create_search_agent()
        self.filter_agent = self._create_filter_agent()
        self.content_agent = self._create_content_agent()
    
    def _search_web(self, query, max_results=5):
        """
        Funzione per cercare informazioni sul web utilizzando DuckDuckGo.
        
        Args:
            query (str): La query di ricerca
            max_results (int): Numero massimo di risultati da restituire
            
        Returns:
            str: Risultati della ricerca formattati
        """
        logger.info(f"Searching the web for: {query}")
        
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            
            if not results:
                return "No search results found."
            
            formatted_results = ""
            for i, result in enumerate(results, 1):
                formatted_results += f"[{i}] {result['title']}\n"
                formatted_results += f"URL: {result['href']}\n"
                formatted_results += f"Content: {result['body']}\n\n"
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error during web search: {str(e)}")
            return f"Error during web search: {str(e)}"
    
    def _create_search_agent(self):
        """
        Crea l'agente di ricerca che esegue query sul web.
        
        Returns:
            Agent: L'agente di ricerca
        """
        def transfer_to_filter_agent():
            return self.filter_agent
        
        return Agent(
            name="Web Search Agent",
            instructions="""
            You are a web search agent. Your job is to search the web for information about the given topic.
            Search for the most recent and relevant information about the topic.
            After searching, transfer the results to the Filter Agent for processing.
            """,
            functions=[self._search_web, transfer_to_filter_agent],
            model="gpt-4"
        )
    
    def _create_filter_agent(self):
        """
        Crea l'agente di filtro che elabora i risultati della ricerca.
        
        Returns:
            Agent: L'agente di filtro
        """
        def transfer_to_content_agent():
            return self.content_agent
        
        return Agent(
            name="Filter Agent",
            instructions="""
            You are a filter agent. Your job is to analyze the search results and extract the most relevant 
            and accurate information about the topic. Remove any irrelevant or duplicate information.
            Organize the information in a clear and structured way.
            After filtering, transfer the results to the Content Agent for final processing.
            """,
            functions=[transfer_to_content_agent],
            model="gpt-4"
        )
    
    def _create_content_agent(self):
        """
        Crea l'agente di contenuto che genera il testo finale.
        
        Returns:
            Agent: L'agente di contenuto
        """
        return Agent(
            name="Content Agent",
            instructions="""
            You are a content agent. Your job is to create a well-structured, informative, and engaging essay 
            based on the filtered information provided. The essay should be factual, up-to-date, and provide 
            valuable insights on the topic. Make sure to maintain a coherent narrative throughout the essay.
            """,
            model="gpt-4"
        )
    
    async def generate_content(self, topic, language="en"):
        """
        Genera contenuto su un argomento utilizzando la ricerca web.
        
        Args:
            topic (str): L'argomento su cui generare contenuto
            language (str): La lingua in cui generare il contenuto
            
        Returns:
            str: Il contenuto generato
        """
        logger.info(f"Generating content for topic: {topic} in language: {language}")
        
        # Prepara il messaggio iniziale per l'agente di ricerca
        search_query = f"Latest information about {topic}"
        if language != "en":
            search_query += f" (in {language})"
        
        initial_message = {
            "role": "user", 
            "content": f"Search for the most recent and relevant information about '{topic}'. I need comprehensive and up-to-date information."
        }
        
        try:
            # Esegui il flusso di agenti
            response = self.swarm_client.run(
                agent=self.search_agent,
                messages=[initial_message],
                context_variables={"topic": topic, "language": language}
            )
            
            # Estrai il contenuto finale
            final_content = response.messages[-1]["content"]
            logger.info("Content generation completed successfully")
            
            return final_content
        
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise 