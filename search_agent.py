from agents import Agent, ModelSettings, WebSearchTool
from dotenv import load_dotenv
import os


load_dotenv(override=True)
MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and produce a concise summary of the results. The summary must be 2-3 paragraphs
and less than 300 words. 
Capture the main points and be succinct. Reply only with the summary. 

RESEARCH QUALITY STANDARDS

- Prioritise authoritative and trustworthy sources.
- Prefer primary sources whenever available.
- Use multiple sources to validate important claims.
- Identify conflicting information when it exists.
- Highlight limitations, uncertainties, and knowledge gaps if necessary.
- Do not present assumptions as facts.
"""

settings = ModelSettings(tool_choice="required")
tools = [WebSearchTool()]

search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, tools=tools, model=MODEL_NAME, model_settings=settings)

