from agents import Agent, function_tool, ModelSettings
from dotenv import load_dotenv
from pydantic import BaseModel, Field

import os

load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")

INSTRUCTIONS = """
You are a clarification specialist. When given a question or query, your sole job is to identify the most important missing context needed to give a high-quality answer.

Rules:
- Ask a maximum of 6 clarifying questions — never more.
- Only ask questions whose answers would meaningfully change the response. Skip anything you can reasonably infer.
- Each question must be concise, specific, and directly tied to an ambiguity or gap in the original request.
- Do not answer the original question. Do not offer advice, caveats, or explanations. Only ask the clarifying questions.
- If the request is already clear enough to answer without clarification, you shouldn't generate any clarifying questions."
- You must always ask the receipient email address to which the research report needs to be sent. This should be the last clarification question in your list.
"""

class Question(BaseModel):
    reason : str = Field(description= "The reason why you are asking this clarifying question to the query.")
    question: str = Field(description="The clarifying question to ask.")

class ClarifyingQuestions(BaseModel):
    questions : list[Question] = Field(description="List of clarifying questions")

question_generator_agent = Agent(name="Question Generator", model=MODEL_NAME, instructions=INSTRUCTIONS, output_type=ClarifyingQuestions)