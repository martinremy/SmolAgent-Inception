#
# Example code to use the diffusion basedInception Model with SmolAgent
#

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

from smolagents import CodeAgent, WebSearchTool, Model, ChatMessage
from smolagents.models import MessageRole

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("INCEPTION_API_KEY")
if api_key is None:
    raise Exception("INCEPTION_API_KEY not found in environment variables")

# Custom model class to handle the Inception API

class InceptionModel(Model):
    def __init__(self, model_id: str, **kwargs):
        super().__init__(model_id=model_id, **kwargs)

    def get_response(self, messages: List[Dict]):
        # Convert ChatMessage objects to dictionaries if needed
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, ChatMessage):
                formatted_messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
            else:
                formatted_messages.append(msg)
        
        response = requests.post(
            'https://api.inceptionlabs.ai/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            },
            json={
                'model': 'mercury',
                'messages': formatted_messages,
                'max_tokens': 1000
            }
        )
        return response

    def generate(
        self,
        messages: List[Dict],
        stop_sequences: Optional[List[str]] = None,
        **kwargs,
    ) -> ChatMessage:
        # Convert smolagents messages -> HF chat format (already close)
        # messages is typically: [{"role": "...", "content": "..."}, ...]
        stop = stop_sequences or []

        response = self.get_response(
            messages=messages
        )
        response_data = response.json()
        content = response_data['choices'][0]['message']['content']
        return ChatMessage(role=MessageRole.ASSISTANT, content=content)


def main():
    model = InceptionModel(model_id="mercury")
    agent = CodeAgent(tools=[WebSearchTool()], model=model, stream_outputs=False)

    print("Welcome! Ask me questions (type 'exit' or 'quit' to stop).\n")

    while True:
        try:
            question = input("Your question: ").strip()

            if question.lower() in ['exit', 'quit', '']:
                print("Goodbye!")
                break

            result = agent.run(question)
            print(f"\nAnswer: {result}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            continue

if __name__ == "__main__":
    main()

