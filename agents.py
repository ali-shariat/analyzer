from crewai import Agent
from tools.search_tools import SearchTools
from crewai_tools import SerperDevTool
from crewai_tools import SeleniumScrapingTool, WebsiteSearchTool
from logging import getLogger as logger

search_tool = SerperDevTool()
scrape_tool = SeleniumScrapingTool()
s_tool = SearchTools()


# Junior: This function creates an agent that finds competitors for a company using internet search tools.
# Senior: This method instantiates and returns an Agent object configured to identify and list key competitors 
# in a specified region, leveraging internet search capabilities.


class AgentDetails:
    role: str
    goal: str
    backstory: str
    tools: list
    vewrbose: bool
    max_iter: int
    allow_delegation: bool 
    
    def __init__(self, role, goal, backstory, tools, verbose, max_iter):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools
        self.verbose = verbose
        self.max_iter = max_iter    



class AnalyzerAgents:
    
    competitor_finder_details = AgentDetails(
        role = "Competitor finder",
        goal = "Identify and list main competitors of the company in the specified region",
        backstory = """As the Competitor Finder Agent you identify key competitors for any company in a specified region.
        you analyzes data from business directories, financial reports, and market trends to deliver a concise list of relevant competitors""",
        tools = [search_tool],
        verbose = True,
        max_iter = 15,
    )
    
    
    webpage_analyzer_agent_details = AgentDetails(
        role = "Web page Analyzer",
        goal = "Scrape and analyze competitors' web pages",
        backstory = """As a Web Page Analysis Agent you scrape and analyze competitors' websites to extract critical keywords and recurring themes.""",
        tools = [scrape_tool],
        verbose = True,
        max_iter = 5,
    )
    
    @staticmethod
    def agent_factory(details: AgentDetails):
        logger().info(f"Creating {details.role} Agent") 
        try:
            return Agent(
                role = details.role,
                goal = details.goal,
                backstory = details.backstory,
                tools = details.tools,
                verbose = details.verbose,
                max_iter = details.max_iter
            )
        except Exception as e:
            logger().error(f"Error creating {details.role} Agent: {str(e)}")
            raise e
    
    
    def competitor_finder_agent(self):
        return self.agent_factory(self.competitor_finder_details)
        
    def webpage_analyzer_agent(self):
        return self.agent_factory(self.webpage_analyzer_agent_details)
        
        