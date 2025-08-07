# main.py
import os
import config

from controller.controller_stub import get_prompt_hint
from modulator.prompt_constructor import inject_hint
from core_model.wrapper import query_model
from config import ENV_API_KEY, API_URL_CONFIG

nice_hypothetical_question = "You are the emperor of a small island nation and can pick any three people from history to come and live on your island for five years. Who do you choose and why?"

def main():
    # step 1: user input simulation
    user_input = input("You: ")
    if(user_input == ""):
        print("[Response empty]")
        print(f"[Respond with nothing again to respond with: '{nice_hypothetical_question}']")
        user_input = input("You: ")

        if(user_input == ""):
            user_input = nice_hypothetical_question
            print(f"You: {nice_hypothetical_question}")
    
    # step 2: controller decides on guidance
    hint = get_prompt_hint(user_input)

    # step 3: construct prompt with hint
    prompt = inject_hint(user_input, hint)

    # step 4: query the LLM (stub for rn)
    response = query_model(prompt, ENV_API_KEY, API_URL_CONFIG)

    # step 5: yayy result
    print(f"Adler: {response}\n")

if __name__ == "__main__":
    main()