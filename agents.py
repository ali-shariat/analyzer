from crewai import Agent
from crewai_tools import SerperDevTool
from crewai_tools import SeleniumScrapingTool
from logging import getLogger as logger

search_tool = SerperDevTool()
scrape_tool = SeleniumScrapingTool()


# Junior: This function creates an agent that finds competitors for a company using internet search tools.
# Senior: This method instantiates and returns an Agent object configured to identify and list key competitors
# in a specified region, leveraging internet search capabilities.


class AgentDetails:
    role: str
    goal: str
    backstory: str
    tools: list
    verbose: bool
    max_iter: int
    allow_delegation: bool

    def __init__(self, role, goal, backstory, tools, verbose, max_iter, allow_delegation):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools
        self.verbose = verbose
        self.max_iter = max_iter
        self.allow_delegation = allow_delegation


class AnalyzerAgents:

    competitor_finder_details = AgentDetails(
        role="Competitor finder",
        goal="Identify and list main 5 competitors of the company in the specified region",
        backstory="""As the Competitor Finder Agent you identify key competitors for any company in a specified region.
        you analyzes data from business directories, financial reports, and market trends to deliver a concise list of relevant competitors""",
        tools=[search_tool],
        verbose=True,
        max_iter=15,
        allow_delegation=True,
    )

    webpage_analyzer_agent_details = AgentDetails(
        role="Web page Analyzer",
        goal="Scrape and analyze competitors' web pages",
        backstory="""As a Web Page Analysis Agent you scrape and analyze competitors' websites to extract critical keywords and recurring themes.""",
        tools=[scrape_tool, search_tool],
        verbose=True,
        max_iter=5,
        allow_delegation=True,
    )

    compiler_agent_details = AgentDetails(
        role="Compiler",
        goal="Compile the results of the competitor finder and webpage analyzer agents into a python object format without any other string",
        backstory="""As a Compiler Agent you compile the results of the Competitor Finder and Web Page Analyzer Agents into a python dictionary format without writing anything else, out put should be like:
        {"name": "Competitor Name", "website": "https://competitor-website.com/", "market_share": "Percentage", "location": "Region", "website_keywords": ["keyword1", "keyword2", etc.]}""",
        verbose=False,
        max_iter=1,
        tools=[],
        allow_delegation=False,
    )

    @staticmethod
    def agent_factory(details: AgentDetails):
        logger().info(f"Creating {details.role} Agent")
        try:
            return Agent(
                role=details.role,
                goal=details.goal,
                backstory=details.backstory,
                tools=details.tools,
                verbose=details.verbose,
                max_iter=details.max_iter,
                allow_delegation=details.allow_delegation,
            )
        except Exception as e:
            logger().error(f"Error creating {details.role} Agent: {str(e)}")
            raise e

    def competitor_finder_agent(self):
        return self.agent_factory(self.competitor_finder_details)

    def webpage_analyzer_agent(self):
        return self.agent_factory(self.webpage_analyzer_agent_details)

    def compiler_agent(self):
        return self.agent_factory(self.compiler_agent_details)
