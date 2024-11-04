from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from query_handler import retrieve
print("Import successful")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; for security, specify your frontend URL if possible
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Server is workin!"}


@app.post("/query")
async def get_answer(request: Request):
    data = await request.json()
    query = data.get("query", "")

    if not query:
        return {"answer": "Please provide a valid question."}

    try:
        # Use retrieve and complete to generate a response
        # prompt = retrieve(query)
        # For now, just return the prompt for testing
        return {"answer": query}
    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"Error during request processing: {e}")
        return {"answer": "An internal error occurred while processing your request."}

    # # Use retrieve and complete to generate a response
    # from query_handler import complete
    # # prompt = retrieve(query)
    # answer = complete("What's a corner?")

    # For testing purposes, just echo back the query in the response
    # return {"answer": {answer}}


