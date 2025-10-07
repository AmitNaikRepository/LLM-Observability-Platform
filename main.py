from fastapi import FastAPI
from observability.tracer import setup_telemetry
from observability.middleware import setup_middleware
from api.routes import router
import uvicorn

app = FastAPI(title="LLM Observability Demo")

# Setup OpenTelemetry
setup_telemetry(app)
setup_middleware(app)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "LLM Observability API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
