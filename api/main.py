from fastapi import FastAPI

app = FastAPI(title="Space Mission Assistant")


@app.get("/")
def root():
    return {"status": "ok"}


# TODO: add endpoints for prediction, RAG query, and agent decision
