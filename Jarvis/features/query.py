from ai71 import AI71

AI71_API_KEY = "YOUR_API_KEY"
client = AI71(AI71_API_KEY)


def ai(command):
    """
    Query the AI client with a command
    :param command: The command or question to be sent to the AI
    :return: The AI's response
    """
    try:
        response = client.chat.completions.create(
            model="tiiuae/falcon-180B-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": command},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"
