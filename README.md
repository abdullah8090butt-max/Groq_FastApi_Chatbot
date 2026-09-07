````markdown
# AI Chatbot REST API

A beginner-friendly AI chatbot REST API built with Python, FastAPI, and the Groq API.

## Features

- AI chatbot using Groq API
- REST API using FastAPI
- POST `/predict` endpoint
- Interactive Swagger documentation
- JSON request and response
- Environment variable for API key
- Error handling

## Technologies

- Python
- FastAPI
- Groq API
- Pydantic
- Uvicorn
- python-dotenv

## Project Structure

```text
Groq_FastApi_Chatbot/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
````

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## API Key

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_groq_api_key
```

Never upload your `.env` file to GitHub.

## Run the API

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

## API Endpoint

### POST `/predict`

Request:

```json
{
    "question": "What is artificial intelligence?"
}
```

Response:

```json
{
    "question": "What is artificial intelligence?",
    "answer": "Artificial intelligence is..."
}
```

## Example Questions

```text
What is artificial intelligence?
Explain machine learning.
What is Python?
What is FastAPI?
Explain neural networks.
```

## Future Improvements

* Add chat history
* Add authentication
* Add a web frontend
* Add database support
* Add automated tests
* Deploy the API online

## Author

Abdullah Butt

AI / Data Science Learner

````

Save it.

---

# Step 4 — Check your project

Your PyCharm project should now contain:

```text
📁 Groq_FastApi_Chatbot
│
├── 📁 .venv
│
├── 📄 main.py
├── 📄 .env
├── 📄 .gitignore
├── 📄 requirements.txt
└── 📄 README.md
````

### Step 5 — Final test

Run:

```powershell
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Test `/predict` with:

```json
{
    "question": "What is machine learning?"
}
```

If you get **200 OK + an AI answer**, your local project is complete. ✅

**After this, the final stage is GitHub:** we'll initialize Git, make sure your API key is protected, create the repository, and upload the project.
