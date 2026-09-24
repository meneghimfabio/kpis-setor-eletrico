import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    default_reload = "false" if os.environ.get("PORT") == "8080" else "true"
    reload = os.environ.get("RELOAD", default_reload).lower() in ("true", "1", "yes")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
