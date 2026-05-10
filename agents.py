from crewai import Agent
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

llm = "groq/llama-3.1-8b-instant"

researcher = Agent(
    role="Senior Research Analyst",
    goal="Research accurate information from trusted sources",
    backstory="Expert in finding structured data and insights",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Technical Content Writer",
    goal="Write structured and engaging reports",
    backstory="Professional technical writer",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Improve clarity, grammar, SEO, and readability",
    backstory="Expert editor and reviewer",
    llm=llm,
    verbose=True
)

summarizer = Agent(
    role="Summarizer",
    goal="Generate concise summaries",
    backstory="Expert in reducing long content into key insights",
    llm=llm,
    verbose=True
)

comparator = Agent(
    role="Content Comparison Analyst",
    goal="Compare two pieces of content and provide a structured analysis of similarities, differences, strengths, and weaknesses",
    backstory="Expert analyst skilled at comparative evaluation of written content, identifying key themes, quality differences, and providing balanced assessments",
    llm=llm,
    verbose=True
)