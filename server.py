"""Start the local chat backend (also serves the frontend at port 8000)."""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("optibot.web:app", host="127.0.0.1", port=8000)
