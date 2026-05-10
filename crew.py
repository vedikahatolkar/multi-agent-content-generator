from crewai import Crew, Process, Task
from tasks import research_task, write_task
from agents import researcher, writer, comparator

from tenacity import retry, stop_after_attempt, wait_fixed

@retry(
stop=stop_after_attempt(3),
wait=wait_fixed(15)
)
def run_crew(topic):

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential
    )

    result = crew.kickoff(inputs={"topic": topic})
    return result


@retry(
stop=stop_after_attempt(3),
wait=wait_fixed(15)
)
def compare_papers(paper_a_content, paper_b_content, topic_a, topic_b):
    """Run a comparison agent on two generated papers."""

    compare_task = Task(
        description=f"""
Compare the following two content papers and provide a detailed analysis.

**Paper A — "{topic_a}":**
{paper_a_content}

**Paper B — "{topic_b}":**
{paper_b_content}

Provide a structured comparison covering:
- Key themes in each paper
- Similarities between the two
- Differences between the two
- Strengths of each paper
- Weaknesses of each paper
- Overall verdict: which paper is stronger and why

Keep your analysis balanced, professional, and concise.
""",
        expected_output="""
A structured comparison report with sections:
Themes, Similarities, Differences, Strengths, Weaknesses, and Verdict.
""",
        agent=comparator
    )

    crew = Crew(
        agents=[comparator],
        tasks=[compare_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    return result
