# Amazon Bedrock

Amazon Bedrock is an easy way to get a bunch of foundational language models setup, such as Titan, AI21, Anthropic, Cohere, etc.

For example:
![APT Dragon](aptdragon.png)
``A dragon made in bedrock.``

To use bedrock in a programmatic fashion:
```
import boto3

# Create a client for the Bedrock service
client = boto3.client('bedrock', region_name='us-east-1')

# Define the input text prompt
prompt = "Generate a creative story about a future city."

# Make a call to Bedrock to generate text
response = client.invoke_model(
    modelId='amazon.titan-text-gen',
    payload={
        'input': prompt
    }
)

# Output the generated text
generated_text = response['output']
print(generated_text)
```