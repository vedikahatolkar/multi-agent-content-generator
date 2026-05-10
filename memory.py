conversation_history = []


def save_memory(user_input, ai_response):
    conversation_history.append({
        "user": user_input,
        "response": ai_response
    })



def get_memory():
    return conversation_history