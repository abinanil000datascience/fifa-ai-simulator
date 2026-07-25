import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from src.agent import (
    get_team_stats_tool,
    search_tactical_news_tool,
    simulate_match_tool
)

def process_user_query(query: str) -> dict:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            temperature=0.3
        )
    except Exception as e:
        return {"query": query, "response": f"Failed to initialize Gemini. Error: {e}"}
    
    tools = [
        get_team_stats_tool,
        search_tactical_news_tool,
        simulate_match_tool
    ]

    # Concise prompt directing the AI to format clean markdown output
    system_prompt = (
        "You are an elite FIFA World Cup 2026 AI Sports Analyst.\n"
        "Always provide clean, direct, concise Markdown answers using bullet points, headers, and bold text.\n"
        "Do not write long, repetitive paragraphs. Avoid unnecessary explanations unless explicitly asked."
    )

    agent = create_react_agent(llm, tools, prompt=system_prompt)

    try:
        result = agent.invoke({"messages": [("user", query)]})
        
        # Safely extract text string whether content is a string or list of dicts
        raw_content = result["messages"][-1].content
        
        if isinstance(raw_content, list):
            text_parts = [block["text"] for block in raw_content if isinstance(block, dict) and block.get("type") == "text"]
            final_response = "\n".join(text_parts) if text_parts else str(raw_content)
        else:
            final_response = str(raw_content)
            
    except Exception as e:
        final_response = f"An error occurred while processing the request: {e}"

    return {
        "query": query,
        "response": final_response
    }

if __name__ == "__main__":
    res = process_user_query("Simulate a match between Argentina and England")
    print(res["response"])