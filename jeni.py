!pip install Flask pyngrok
#ull need groksdeployment key to begin with along with open ais api
from flask import Flask, request, render_template_string
from openai import AzureOpenAI
from google.colab import userdata
from pyngrok import ngrok

# Azure OpenAI endpoint and deployment details
endpoint = "https://gpt4ohackathon.openai.azure.com/"
deployment_name = "gpt-4o"

# Create the AzureOpenAI client
client = AzureOpenAI(
    api_key=userdata.get("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

app = Flask(__name__)

def generate_story(prompt):
    response = client.chat.completions.create(
        model=deployment_name,
        max_tokens=300,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Check if the response is OK and print out the response
    if response and hasattr(response, 'choices') and len(response.choices) > 0:
        return response.choices[0].message.content.strip()
    else:
        return "No valid response received."

@app.route('/', methods=['GET', 'POST'])
def home():
    story = ""
    if request.method == 'POST':
        prompt = request.form['prompt']
        story = generate_story(prompt)
    return render_template_string('''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Story Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #fff;
            color: #000;
            padding-top: 5rem;
        }
        .container {
            max-width: 800px;
            margin: auto;
            text-align: center;
        }
        .form-container {
            background-color: #fff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .form-label {
            font-weight: 700;
        }
        .form-control {
            margin-bottom: 1rem;
        }
        .btn {
            background-color: #000;
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            font-size: 1rem;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #333;
        }
        .generated-story {
            margin-top: 20px;
            background-color: #fff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-container">
            <h1 class="display-4 mb-4">Story Generator</h1>
            <form method="post">
                <div class="mb-3">
                    <label for="prompt" class="form-label">Enter a prompt:</label>
                    <input type="text" class="form-control" id="prompt" name="prompt" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Generate Story</button>
            </form>
        </div>
        {% if story %}
            <div class="generated-story">
                <h2 class="mb-4">Generated Story:</h2>
                <p>{{ story }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>

    ''', story=story)

# Start ngrok and expose the local server
public_url = ngrok.connect(5000)
print(f'Public URL: {public_url}')

# Run the Flask app
app.run(port=5000)
