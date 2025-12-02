# AI Trip Planner

An intelligent travel planning application with AI-powered trip recommendations, expense calculations, and real-time information gathering.

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- `uv` package manager (optional but recommended)

### 2. Install uv (if not already installed)

```bash
pip install uv
```

### 3. Create Virtual Environment

```bash
# If you have conda, first deactivate it
conda deactivate

# Create virtual environment
uv venv env --python cpython-3.10.18-windows-x86_64-none
```

### 4. Activate Virtual Environment

**Windows:**
```bash
.\env\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### 5. Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or using uv
uv pip install -r requirements.txt
```

### 6. Environment Variables Setup

Create a `.env` file in the project root with the following API keys:

```env
# Required - LLM Provider API Key (choose one)
GOOGLE_API_KEY=your_google_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
# OR
GROQ_API_KEY=your_groq_api_key_here

# Optional - For enhanced features
GPLACES_API_KEY=your_google_places_api_key_here
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key_here
```

**Where to get API keys:**
- **GOOGLE_API_KEY**: https://makersuite.google.com/app/apikey (for Gemini)
- **OPENAI_API_KEY**: https://platform.openai.com/api-keys
- **GROQ_API_KEY**: https://console.groq.com/
- **GPLACES_API_KEY**: https://console.cloud.google.com/
- **OPENWEATHERMAP_API_KEY**: https://openweathermap.org/api
- **TAVILY_API_KEY**: https://tavily.com/
- **ALPHAVANTAGE_API_KEY**: https://www.alphavantage.co/support/#api-key

> **Note**: At minimum, you need `GOOGLE_API_KEY` (default), `OPENAI_API_KEY`, or `GROQ_API_KEY` for the application to work. Other keys are optional but enable additional features. The default provider is **Google Gemini**.

## Running the Application

### Run Backend (FastAPI)

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at: `http://localhost:8000`

### Run Frontend (Streamlit)

In a **separate terminal** (with virtual environment activated):

```bash
streamlit run streamlit_app.py
```

The frontend will be available at: `http://localhost:8501`

### Run Both Simultaneously

1. Open **Terminal 1**: Activate virtual environment and run backend
   ```bash
   .\env\Scripts\activate.bat
   uvicorn main:app --reload --port 8000
   ```

2. Open **Terminal 2**: Activate virtual environment and run frontend
   ```bash
   .\env\Scripts\activate.bat
   streamlit run streamlit_app.py
   ```

## Troubleshooting

### Error: "GOOGLE_API_KEY environment variable is not set"

**Solution**: Create a `.env` file in the project root and add your API key:
```env
GOOGLE_API_KEY=your_actual_google_api_key_here
```

**Note**: The application uses Google Gemini by default. If you want to use a different provider, you can change the `model_provider` parameter in `main.py` and `agent/agentic_workflow.py`.

### Error: "uvicorn is not recognized"

**Solution**: Make sure you've activated the virtual environment and installed dependencies:
```bash
.\env\Scripts\activate.bat
pip install -r requirements.txt
```

### Error: 500 Internal Server Error

**Common causes:**
1. Missing API keys in `.env` file
2. Invalid API key
3. Network connectivity issues

Check the terminal output for detailed error messages. The improved error handling will now show specific error details.

### Error: Model decommissioned or API errors

**Solution**: If using Groq or OpenAI and getting model decommissioned errors, you can switch to Google Gemini (default) or update the model name in `config/config.yaml`.

**Available Gemini Models:**
- `gemini-1.5-pro` (default, recommended for best quality)
- `gemini-1.5-flash` (faster, good quality)
- `gemini-pro`

Check [Google's documentation](https://ai.google.dev/models/gemini) for the latest available models.