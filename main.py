from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# 🔑 Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# 🔹 External Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🔹 Model Config
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

print("Weather Expert by Mohib Ali Khan")

cityname = input("Enter City name 🌍☁️: ")

# 🎯 1) Normal Text Output Agent
agent_text = Agent(
    name="Weather Text Agent",
    instructions="""
    Tum ek Weather Agent ho. Jab bhi me kisi city ka weather pochun, tum mujhe sirf ye cheezen batao:
    The weather in location is Weather Condition, Temperature in °C.
    """
)

result_text = Runner.run_sync(agent_text, input=cityname, run_config=config)
print("\n📌 Normal Agent Output:")
print(result_text.final_output)

# 🎯 2) Structured Output Agent (dataclass)
@dataclass
class WeatherReport:
    temperature: float
    condition: str
    location: str

agent_structured = Agent(
    name="Weather Structured Agent",
    instructions="""
    Tum ek Weather Agent ho. Jab bhi me kisi city ka weather pochun, tum mujhe sirf ye cheezen batao:
    """,
    output_type=WeatherReport
)

result_structured = Runner.run_sync(agent_structured, input=cityname, run_config=config)
weather: WeatherReport = result_structured.final_output

print("\n📌 Structured Agent Output:")
print("Temperature:", weather.temperature, "°C")
print("Condition:", weather.condition)
print("Location:", weather.location)
