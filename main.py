from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AnalyzerAgents
from tasks import AnalyzerTasks
from dotenv import load_dotenv
from file_io import save_markdown
from fastapi import FastAPI
import json


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
            compiler = agents.compiler_agent()
        except Exception as e:
            print(f"Error creating agents: {str(e)}")
            return
        # Instantiate the tasks
        # comment
        competitor_finder_task = tasks.competitor_finder_task(
            competitor_finder, self.company, self.region
        )
        webpage_analyzer_task = tasks.webpage_analyzer_task(
            webpage_analyzer, [competitor_finder_task]
        )
        compiler_task = tasks.compiler_task(
            compiler, [competitor_finder_task, webpage_analyzer_task], save_markdown)
        # Form the crew
        crew = Crew(
            agents=[competitor_finder, webpage_analyzer, compiler],
            tasks=[competitor_finder_task,
                   webpage_analyzer_task, compiler_task],
            process=Process.hierarchical,
            manager_llm=OpenAIGPT4,
            verbose=True,
        )

        result = crew.kickoff()
        return result

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Welcome to Competitive Intelligence Analyzer"}
@app.get("/analyze/{company}/{region}")
def get_company_name_and_region(company: str, region: str):
    analyzer_crew = AnalyzerCrew(company, region)
    result = analyzer_crew.run()
    
    if not result:
        return {"error": "Analysis failed"}
    
    # Log raw result before parsing
    print(f"Raw result from crew: {result.raw}")
    
    try:
        return json.loads(result.raw)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return {"error": f"Invalid JSON: {e}"}
    
