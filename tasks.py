from crewai import Task
from datetime import datetime


        
class AnalyzerTasks:
    
    def competitor_finder_task(self, agent, company, region):
        print(f"Creating Competitor Finder Task for {company} in {region}")
        return Task(
            description=f"Identify and list main competitors of {company} in {region}",
            agent=agent,
            expected_output="""
                "competitors": [
                    {
                        "name": "Competitor Name",
                        "website": "https://competitor-website.com",
                        "market_share": "Percentage",
                        "location": "Region"
                    }
                ]
            """,
            async_execution=False,
        )

    def webpage_analyzer_task(self, agent, context):
        print("Creating Webpage Analyzer Task with context:")
        print(context)
        return Task(
            description="Analyze the given webpage context",
            agent=agent,
            context=context,
            expected_output="""
                "analysis": {
                    "title": "Webpage Title",
                    "content": "Main content of the webpage",
                    "keywords": ["keyword1", "keyword2"]
                }
            """,
             async_execution=False,

        )
