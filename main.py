from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
load_dotenv()

# Error handling imports
try:
    from groq import BadRequestError as GroqBadRequestError
except ImportError:
    GroqBadRequestError = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print(f"Received query: {query.question}")
        graph = GraphBuilder(model_provider="gemini")
        react_app=graph()
        #react_app = graph.build_graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Convert string question to proper LangChain message format
        messages={"messages": [HumanMessage(content=query.question)]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except ValueError as e:
        # Handle configuration/API key errors
        error_msg = str(e)
        print(f"Configuration error: {error_msg}")
        return JSONResponse(status_code=400, content={"error": error_msg, "type": "configuration_error"})
    except Exception as e:
        # Handle API errors
        error_msg = str(e)
        error_type = "server_error"
        
        # Check if it's a Groq API error (for backward compatibility)
        if GroqBadRequestError and isinstance(e, GroqBadRequestError):
            error_type = "api_error"
            if "model_decommissioned" in error_msg or "decommissioned" in error_msg.lower():
                error_msg = "The configured model has been decommissioned. Please update the model name in config/config.yaml."
        
        print(f"Error processing query: {error_msg}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=400 if error_type == "api_error" else 500, 
                          content={"error": error_msg, "type": error_type})