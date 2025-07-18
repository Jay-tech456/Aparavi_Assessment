from flask import Flask, Response, request, jsonify
import time
import json
from flask_cors import CORS
from langchain_core.messages import HumanMessage
from Workflow.workflow import workflow

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "http://localhost:3000"}}, supports_credentials=True)


graph_instance = workflow()
graph = graph_instance.get_graph()

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})

@app.route('/ask', methods=['POST'])
def ask_agent():
    def generate():
        try:
            # Simulate agent streaming output
            for chunk in ["This is ", "a streamed ", "response"]:
                yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
                time.sleep(0.5)

            yield "data: {\"type\":\"done\"}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)