from agents import Agent, Runner, function_tool, ModelSettings
from agents.repl import run_demo_loop
import asyncio
from dotenv import load_dotenv
import os
from clarification_question_generator_agent import question_generator_agent


load_dotenv(override=True)

@function_tool(needs_approval=True)
async def multiply(num1: int, num2: int) -> int:
    """ Tool to multiple two numbers. """
    print("Inside multiple tool.")
    return (num1 * num2)

tools = [multiply]

repl_agent = Agent(
    name="Talk To me",
    instructions="You are an agent great at all the mathematical calculations",
    model="gpt-5.4-mini",
    tools=tools,
    model_settings=ModelSettings(tool_choice="required")
)

# asyncio.run(run_demo_loop(agent=repl_agent, stream=True))

history = []

message = {
    "role": "user",
    "content": "What is the value of 2 * 2?"
}

history.append(message)

async def run():
    response = await Runner.run(repl_agent, input=history)
    #print(response.interruptions)
    # GET THE CURRENT STATE OF THE AGENT
    state = response.to_state()
    #state.approve(ToolapprovalItem)
    print(response.to_state())
    print(response.agent_tool_invocation)
    print(response.final_output)

async def question_generator():
    response = await Runner.run(question_generator_agent, input="I want to sleep")
    print(response.final_output)






#asyncio.run(run())
asyncio.run(question_generator())