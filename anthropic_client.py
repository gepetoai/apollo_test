import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=250,
    temperature=0,
    system="",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "[intentionally left blank because the first message is from you, the assistant]"
                }
            ]
        }
    ]
)
print(message.content)