from crewai import Crew, Agent, Task, Pipeline

# Define your crews
research_crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential
)

analysis_crew = Crew(
    agents=[analyst],
    tasks=[analysis_task],
    process=Process.sequential
)

writing_crew = Crew(
    agents=[writer],
    tasks=[writing_task],
    process=Process.sequential
)

# Assemble the pipeline
my_pipeline = Pipeline(
    stages=[research_crew, analysis_crew, writing_crew]
)