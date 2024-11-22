from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AnalyzerAgents
from tasks import AnalyzerTasks
from dotenv import load_dotenv

load_dotenv()
OpenAIGPT4 = ChatOpenAI(model="gpt-4o")


class AnalyzerCrew:
    def __init__(self, company, region):
        self.region = region
        self.company = company

    def run(self):
        # Initialize the agents and tasks
        agents = AnalyzerAgents()
        tasks = AnalyzerTasks()
        # Instantiate the agents
        try:
            competitor_finder = agents.competitor_finder_agent()
            webpage_analyzer = agents.webpage_analyzer_agent()
        except Exception as e:
            print(f"Error creating agents: {str(e)}")
            return
        # Instantiate the tasks
        competitor_finder_task = tasks.competitor_finder_task(
            competitor_finder, self.company, self.region
        )
        webpage_analyzer_task = tasks.webpage_analyzer_task(
            webpage_analyzer, [competitor_finder_task]
        )
        # Form the crew
        crew = Crew(
            agents=[competitor_finder, webpage_analyzer],
            tasks=[competitor_finder_task, webpage_analyzer_task],
            process=Process.hierarchical,
            manager_llm=OpenAIGPT4,
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to Competitive Intelligence Analyzer")
    print("-------------------------------")
    company = input(
        (
            """
      Please enter the name of the company:
    """
        )
    )
    region = input(
        (
            """
      Enter the region or country where the company operates:
    """
        )
    )

    analyzer_crew = AnalyzerCrew(company, region)
    result = analyzer_crew.run()
    print("\n\n########################")
    print(
        f"## Here is the competitive intelligence analysis for {company} in {region}:"
    )
    print("########################\n")
    print(result)
