from flask import Flask, request, jsonify
from flask_cors import CORS
from ai71 import AI71

app = Flask(__name__)
CORS(app)  # This will allow all origins. For production, configure this carefully.

AI71_API_KEY = "ai71-api-d26be421-3d0c-4315-89f6-02cc5ee1d80a"
client = AI71(AI71_API_KEY)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.append({"role": "user", "content": user_message})
    
    content = ""
    for chunk in client.chat.completions.create(
        messages=messages,
        model="tiiuae/falcon-180B-chat",
        stream=True
    ):
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            content += delta_content
    
    messages.append({"role": "assistant", "content": content})
    return jsonify({"response": content})

if __name__ == '__main__':
    app.run(debug=True)
