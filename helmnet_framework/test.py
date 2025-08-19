from feedback.evaluator import evaluate_controller_decision
from config import ENV_API_KEY, API_URL_CONFIG

user_input = "You are the emperor of a small island nation and can pick any three people from history to come and live on your island for five years. Who do you choose and why?"

controller_tokens = "[reflect] [query]"

llm_response = (
    "[Reflect: The user is asking for a creative and personal choice, so I should consider historical figures "
    "who would bring diverse skills, wisdom, and perspectives to enrich the island nation, while also justifying my selections with clear reasoning.]\n\n"
    "[Query: I would choose Leonardo da Vinci for his unparalleled creativity and inventiveness, as his skills in art, science, and engineering "
    "could inspire innovation and cultural growth on the island.]"
)

evaluate_controller_decision(user_input, controller_tokens, llm_response, ENV_API_KEY, API_URL_CONFIG)
