from __future__ import annotations

import sys
import webbrowser
import threading
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="ER Editor")

# Import and configure routes (needs model_path at startup)
from api.routes import router, set_model_path
app.include_router(router, prefix="/api")

# Static files (must be last -- catches all unmatched paths)
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")


def open_browser():
    webbrowser.open("http://localhost:8000")


if __name__ == "__main__":
    import uvicorn
    if len(sys.argv) < 2:
        print("Usage: python server.py /path/to/model.py")
        sys.exit(1)
    model_path = Path(sys.argv[1]).resolve()
    if not model_path.exists():
        print(f"Error: File not found: {model_path}")
        sys.exit(1)
    set_model_path(model_path)
    threading.Timer(1.0, open_browser).start()
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
