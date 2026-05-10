from crewai import Task
from agents import researcher, writer

research_task = Task(

description="""
Research the topic: {topic}

Gather:
- important insights
- examples
- factual information
- recent developments

ALSO include 3 useful reference links
from reliable websites related to the topic.

Keep the research structured.
""",

expected_output="""
Structured research notes with useful reference links.
""",

agent=researcher


)


write_task = Task(


description="""
Using the research provided,
generate high-quality content appropriate for the topic.

The writing style, structure, and tone should adapt
naturally based on the topic provided.

Examples:
- debates → argumentative structure
- technical topics → explanatory structure
- business topics → professional style
- educational topics → beginner-friendly explanation

Make the content engaging, clear, and well-structured.
""",

expected_output="""
Well-structured content dynamically adapted to the topic.
""",

agent=writer

)
