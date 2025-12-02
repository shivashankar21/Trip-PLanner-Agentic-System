# 🚀 Trip-PLanner-Agentic-System

An intelligent **AI-powered travel planning system** that uses an **agentic workflow**, modular tools, and real-time APIs to generate end-to-end trip planning assistance. The system can:

* Search places
* Fetch live weather
* Perform expense calculations
* Convert currencies
* Generate travel documents
* Use an agent LLM to orchestrate tools
* Expose a backend API + Streamlit frontend

This README explains **project features**, **architecture**, **code flow**, and **how the system works internally**.

---

# 🌐 System Overview

The Trip-PLanner-Agentic-System is built around an **LLM-driven agent** that invokes modular tools depending on the user query. The agent breaks down user requests, selects the proper tools from the `/tools` module, gathers data from `/utils` helpers, and composes a final structured response.

---

# 📁 Project Structure (Explained)

Your folder structure (from images) is summarized and explained below:

```
Trip-PLanner-Agentic-System/
│
├── agent/
│   ├── agentic_workflow.py      # Core agent engine - tool calling, reasoning, planning
│   └── __init__.py
│
├── tools/                       # Tool interface layer (LLM-callable tools)
│   ├── arthamatic_op_tool.py
│   ├── currency_conversion_tool.py
│   ├── expense_calculator_tool.py
│   ├── place_search_tool.py
│   └── weather_info_tool.py
│
├── utils/                       # Internal functional modules
│   ├── config_loader.py
│   ├── currency_converter.py
│   ├── expense_calculator.py
│   ├── model_loader.py
│   ├── place_info_search.py
│   ├── save_to_document.py
│   └── weather_info.py
│
├── prompt_library/
│   ├── prompt.py                # All prompt templates for LLM agent
│
├── config/
│   ├── config.yaml              # Model provider & API config
│
├── logger/                      # Logging
│   ├── logging.py
│
├── main.py                      # FastAPI backend entrypoint
├── streamlit_app.py             # Streamlit UI
├── requirements.txt
├── README.md
└── .env
```

---

# 🧠 Core Functional Flow

Below is the **high-level flow** of how your Trip Planner works end-to-end:

### **1. User Input (UI or API)**

User enters something like:

> "Plan a 3-day trip to Manali with budget estimation and weather details."

### **2. Request → FastAPI backend (`main.py`)**

`main.py` receives the request and hands it to the **agent system**.

### **3. Agentic Workflow (`agent/agentic_workflow.py`)**

The agent does:

1. Understands user intent
2. Breaks into subtasks
3. Chooses tools dynamically
4. Calls tools using proper function schemas
5. Aggregates responses
6. Generates a final plan with reasoning

### **4. Tools Layer (`/tools`)**

Each tool only does **one job**:

| Tool                          | Function                     |
| ----------------------------- | ---------------------------- |
| `place_search_tool.py`        | Search places & attractions  |
| `weather_info_tool.py`        | Fetch live weather           |
| `expense_calculator_tool.py`  | Calculate trip expenses      |
| `currency_conversion_tool.py` | Convert currencies           |
| `arthamatic_op_tool.py`       | Basic helper math operations |

The agent calls these as external functions.

### **5. Utils Layer (`/utils`)**

These are **actual implementations** of business logic:

| Utility                 | Purpose                            |
| ----------------------- | ---------------------------------- |
| `place_info_search.py`  | Google Places API wrapper          |
| `weather_info.py`       | OpenWeather API wrapper            |
| `expense_calculator.py` | Expense computation                |
| `currency_converter.py` | Currency API wrapper               |
| `save_to_document.py`   | Export trip plan as a document     |
| `model_loader.py`       | Loads LLM provider based on `.env` |
| `config_loader.py`      | Loads YAML-based settings          |

All tools act as **adapters on top of utils**.

### **6. Response Assembly**

Agent synthesizes collected data into:

✔ Trip plan
✔ Itinerary
✔ Budget estimation
✔ Weather summary
✔ Transport suggestions
✔ Optional downloadable document

---

# 🧬 Code Flow Explanation (Detailed)

## **1. Entry Layer**

### `main.py`

* Creates FastAPI app
* Loads environment configs
* Provides API routes:

  * `/plan-trip`
  * `/calculate-expense`
  * `/search-place`
* Passes input to the agent
* Returns JSON output

---

## **2. Agent Layer**

### `agent/agentic_workflow.py`

This is the brain of the entire system.

**Responsibilities:**

* Loads LLM from `utils/model_loader.py`
* Loads tool definitions from `/tools`
* Defines agent instructions (from `prompt_library/prompt.py`)
* Supports:

  * multi-step reasoning
  * tool calling
  * structured output formatting
* Handles errors gracefully

Workflow:

```
User Query → Agent → Reasoning → Picks Tool → Executes Tool → Aggregates Data → Final Trip Plan
```

---

## **3. Tools Layer**

Each file in `/tools` represents a **schema-defined tool function** that the LLM can call.
Example tools:

### `currency_conversion_tool.py`

Defines:

* parameters
* description
* response schema
  But internally uses → `utils/currency_converter.py`.

### `place_search_tool.py`

High-level wrapper for → `utils/place_info_search.py`.

💡 **Tools never contain business logic** — they only expose functions to the agent.

---

## **4. Utils Layer**

Actual functional implementations.

### `weather_info.py`

* Calls OpenWeatherMap API
* Cleans data
* Returns structured dictionary

### `expense_calculator.py`

* Calculates:

  * travel cost
  * stay cost
  * food cost
  * misc cost
* Aggregates into final budget

### `save_to_document.py`

Exports trip details into:

* PDF
* DOCX
* TXT
  (depending on implementation)

---

## **5. Prompt Layer**

### `prompt_library/prompt.py`

Contains:

* System prompts
* Tool-use instructions
* Output formatting templates
* Agent guidelines

Helps maintain clean separation between **logic** and **instructions**.

---

## **6. Config Layer**

### `config/config.yaml`

Stores all configurable values such as:

* LLM model provider
* Default model name
* Temperature
* API timeout
* Enabled tools

You can switch between:

* Gemini
* OpenAI
* Groq

without modifying the code.

---

# ⚙️ Setup Instructions

(Your original instructions have been kept but improved.)

### **1. Prerequisites**

* Python 3.10+
* uv (recommended)
* API keys (Google/OpenAI/Groq)

---

### **2. Install uv**

```bash
pip install uv
```

---

### **3. Create a Virtual Environment**

```bash
uv venv env --python cpython-3.10.18-windows-x86_64-none
```

---

### **4. Activate Environment**

**Windows**

```bash
.\env\Scripts\activate.bat
```

**Linux/Mac**

```bash
source env/bin/activate
```

---

### **5. Install Requirements**

```bash
uv pip install -r requirements.txt
```

---

### **6. Create a `.env` File**

```env
GOOGLE_API_KEY=your_key
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
GPLACES_API_KEY=your_key
OPENWEATHERMAP_API_KEY=your_key
TAVILY_API_KEY=your_key
ALPHAVANTAGE_API_KEY=your_key
```

---

# ▶️ Running the Application

### **Start Backend**

```bash
uvicorn main:app --reload --port 8000
```

### **Start Frontend**

```bash
streamlit run streamlit_app.py
```

---

# 🛠 Troubleshooting

### Missing API Key

Add the key in `.env`.

### Model Not Available

Change provider in `config/config.yaml`.

### uvicorn Not Recognized

Activate environment again.

---

# 🎯 Features Summary

| Feature            | Description                          |
| ------------------ | ------------------------------------ |
| Agentic LLM        | Intelligent reasoning & tool calling |
| Place Search       | Uses Google Places API               |
| Weather Info       | Live weather reports                 |
| Expense Calculator | Full trip budget breakdown           |
| Currency Converter | Rate lookups via API                 |
| Document Export    | Save trip plan                       |
| Streamlit App      | Clean UI                             |
| FastAPI Backend    | API architecture                     |

---
<img width="1024" height="1536" alt="ChatGPT Image Dec 2, 2025, 07_59_31 PM" src="https://github.com/user-attachments/assets/bd94bea1-4577-463d-8148-85f411f51359" />



