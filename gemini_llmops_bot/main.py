import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import track_prompt_version, count_tokens
from feedback_logger import log_feedback
from evaluator import evaluate_output
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Define state schema
class BotState(BaseModel):
    question: str
    response: str = ""

# Node function
def answer_question(state: BotState) -> BotState:
    question = state.question

    # Prompt version tracking
    version = track_prompt_version(question)
    print(f"\n🔖 Prompt Version ID: {version}")

    # Token counting
    token_count = count_tokens(question)
    print(f"📏 Estimated Tokens: {token_count}")

    # Gemini answer
    response = model.generate_content(question).text
    print("\n🤖 Gemini Answer:", response)

    # Feedback
    feedback = input("\n📝 Rate this answer (1-5): ")
    log_feedback(question, response, feedback)

    # Evaluation
    evaluate_output(response, expected_quality=4)

    return BotState(question=question, response=response)

# Build LangGraph
builder = StateGraph(BotState)
builder.add_node("ask", answer_question)
builder.set_entry_point("ask")
builder.add_edge("ask", END)  # ✅ REQUIRED
graph = builder.compile()

# Run the bot
user_question = input("💬 Enter your question: ")
result = graph.invoke(BotState(question=user_question))
