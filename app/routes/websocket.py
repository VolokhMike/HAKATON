from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()




@app.get("/")
async def get():
    return HTMLResponse()

# WebSocket эндпоинт
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Вы сказали: {data}")

# 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=30001)