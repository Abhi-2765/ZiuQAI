import uvicorn 

# test routes at: http://localhost:8080/docs

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="localhost", port=8080, reload=True)