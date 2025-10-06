from fastapi import FastAPI

#  criando a app
app = FastAPI()

@app.get("/")
def hello_world():
    return {"mensagem": "OK Mundo"}