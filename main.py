from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner
import search_agent, planner_agent
from research_manager import ResearchManager


load_dotenv(override=True)

async def checkForAPIKey():
    if os.getenv("OPENAI_API_KEY"):
        print("OPENAPI API Key Found.")
    else:
        print("OPENAPI API Key Not Found.")
    
    # agent = Agent(
    #     name= "Gift Suggestor",
    #     instructions="You are an expert in providing suggestions for gifts for any kind of occassions.Do not respond in markdown. Never use markdown formatting.",
    #     model= "gpt-4o-mini"
    # )

    # result = await Runner.run(starting_agent=agent, input="I am going to attend the birthday party of my colleagues father. Suggest a gift for him.")
    # print(result.final_output)


    # agent_test = Agent(
    #     name="Dipak Agent",
    #     instructions="You are night at telling night time jokes. You must wish good night after telling a joke.",
    #     model="gpt-4o-mini"
    # )

    # result2 = await Runner.run(starting_agent= agent_test, input="Tell me a nice joke")
    # print(result2.final_output)

    # response = await Runner.run(search_agent.search_agent, input="What is Accenture share price today?")
    # print(response.final_output)

    researcher = ResearchManager()
    await researcher.run(query="How to loose 30kgs of weight?")

def main():
    print("Hello from openaiagentssdk!")
    asyncio.run(checkForAPIKey())
    print("Execution completed!")


if __name__ == "__main__":
    main()
