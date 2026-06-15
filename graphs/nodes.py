#1. all imports
import json
import os
from openai import OpenAI

from dotenv import load_dotenv

from prompts.prompts import VALIDATE_RISK_PROMPT
from prompts.prompts import GENERATE_RESPONSE_PROMPT

from graphs.state import RiskState

#2. setting up open ai client
load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENROUTER_API_KEY"),
    base_url = "https://openrouter.ai/api/v1"   
)
#3. node 1 : validate risk

def validate_risk(state: RiskState):

    #a. Grab the user_input from the state
    user_input = state["user_input"]
    #b. Call OpenAI using VALIDATE_RISK_PROMPT and the user_input
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b:free",
        messages = [
            {"role": "system", "content": VALIDATE_RISK_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    #c. Read the JSON response from OpenAI
    raw1_response = response.choices[0].message.content
    
    #d. Parse the JSON string into a Python dictionary using json.loads()
    parsed_data = json.loads(raw1_response)
    
    #e. Return the updated state fields
    return {
        "is_valid_risk": parsed_data["is_project_risk"],
        "is_detailed": parsed_data["is_detailed_enough"],
        "followup_questions": parsed_data["followup_questions"],
        "current_step": "validate_risk"
    }

#4. node 2 : generate response

def generate_response(state: RiskState):
    # a. Grab the user_input AND the strategy from the state
    combined_input = f"Risk: {state['user_input']}.Strategy: {state['strategy']}"
    
    # b. Combine them into one string for the AI
    
    # c. Call OpenAI using GENERATE_RESPONSE_PROMPT and the combined string
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b:free",
        messages = [
            {"role": "system", "content": GENERATE_RESPONSE_PROMPT},
            {"role": "user", "content": combined_input}
        ]
    )
    # d. Read the text response from OpenAI
    raw2_response = response.choices[0].message.content
    # e. Return the updated state fields (ai_response, current_step)
    return {
        "ai_response": raw2_response,
        "current_step": "generate_response"
    }




#testing purpose only
if __name__ == "__main__":
    #testing node 1
    print("testing validate_risk\n")
    test_state_1 = {"user_input": "server might crash"}
    result_1 = validate_risk(test_state_1)
    print(result_1)

    #testing node 2
    print("testing generate_response\n")
    test_state_2 = {"user_input": "server might crash", "strategy": "mitigate"}
    result_2 = generate_response(test_state_2)
    print(result_2)