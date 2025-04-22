from langchain_openai import ChatOpenAI
from desktop_agents.agents.browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main_browser_use():
    agent = Agent(
        task="Go to this website 'https://manatoki468.net/comic/22166578' and wait 6 seconds and then when page loads wait anothe 10 seconds",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

# asyncio.run(main_browser_use())