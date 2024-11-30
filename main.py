from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AnalyzerAgents
from tasks import AnalyzerTasks
from dotenv import load_dotenv
from file_io import save_markdown
from fastapi import FastAPI
import json
import requests
from fastapi.middleware.wsgi import WSGIMiddleware
from dash import Dash, dcc, html, Input, Output, callback, State
import uvicorn

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

style = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app_dash = Dash(__name__, requests_pathname_prefix="/dash/",
                external_stylesheets=style) # type: ignore

app_dash.layout = html.Div(children=[
    html.H1(children='Competitive Intelligence Analyzer'),

    html.Div(children='''
        Enter the company name and region to analyze:
    '''),

    dcc.Input(id='input-company', type='text', placeholder='Company Name'),
    dcc.Input(id='input-region', type='text', placeholder='Region'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    html.Div(id='output-container')
])


@app_dash.callback(
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('input-company', 'value'), 
    State('input-region', 'value')
)
def update_output(n_clicks, company, region):
    if n_clicks == 1 and company and region:
        try:
            response = requests.get(
                f"http://127.0.0.1:8000/analyze/{company}/{region}")
            if response.status_code == 200:
                return json.dumps(response.json(), indent=4)
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception: {e}"
    return "Enter the company name and region, then click Submit."


app.mount("/dash", WSGIMiddleware(app_dash.server))

if __name__ == "__main__":
    uvicorn.run(app)
