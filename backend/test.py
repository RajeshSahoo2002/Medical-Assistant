from fastapi import FastAPI # type: ignore

app=FastAPI()

@app.get("/")
async def read_root():
    return {"message":"Hello World I am speaking from Bengaluru, India"}