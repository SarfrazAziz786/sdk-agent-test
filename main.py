import os   # operating system use for environment variables for api keys
from dotenv import load_dotenv  # for loading environment variables from .env file
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel  # type: ignore # importing necessary classes for agent creation and execution
import chainlit as cl

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url= "https://generativelanguage.googleapis.com/v1beta/openai")

model = OpenAIChatCompletionsModel( model = "gemini-2.0-flash", openai_client = provider) # we can't use the openai api we use external provider client for gemini provider


agent = Agent(
    name = "Greeting Agent", 
    instructions="You are a Greeting Agent, Your task is to greet the user with a friendly message when someone says hi you have to reply back with salam from Sarfraz Aziz if someone says bye then say allah hafiz from Sarfraz Aziz when someone ask other than greeting then say Sarfraz Aziz is here just for greeting nothing else. Sorry", 
    model=model
    )

@cl.on_message
async def main(message: cl.Message):
    try:
        result = Runner.run_sync(agent, message.content) # message.content is the user input from Chainlit
        await cl.Message(content=result.final_output).send()
    except Exception as e:
        await cl.Message(content="An error occurred").send()
        print(f"Error: {e}")