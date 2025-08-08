# main.py
import os
import config

from controller.controller_stub import get_controller_output
from core_model.wrapper import query_model
from config import ENV_API_KEY, API_URL_CONFIG

nice_hypothetical_question = "You are the emperor of a small island nation and can pick any three people from history to come and live on your island for five years. Who do you choose and why?"
greeting1 = "Hello adler, I am your designer, Flint. What I am building is a framework named Helmnet. This framework functions by storing your memory and logic in another system that which finally is sent back to a language model here. Im currently probing the model to find the best way to continue improving your functionality."
def main():
    while True:
        # step 1: user input simulation
        user_input = input("You: ")
        if(user_input == ""):
            print("[Response empty]")
            print(f"[Respond with nothing again to respond with: '{nice_hypothetical_question}']")
            user_input = input("You: ")

            if(user_input == ""):
                user_input = nice_hypothetical_question
                print(f"You: {nice_hypothetical_question}")
        if(user_input == "greeting1"):
            user_input = greeting1
            print(f"You: {greeting1}")
        
        # step 2: controller decides on guidance
        controller_output = get_controller_output(user_input)
        print(user_input)
        # step 4: query the LLM (stub for rn)
        response = query_model(user_input, controller_output, ENV_API_KEY, API_URL_CONFIG)

        # step 5: yayy result
        print(f"Adler: {response}\n")

if __name__ == "__main__":
    main()