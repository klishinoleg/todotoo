from pathlib import Path

import uvicorn

APP_DIR = Path(__file__).resolve().parent / "app"


if __name__ == "__main__":
    uvicorn.run(
        "interfaces.fast_api.main:app",
        app_dir=str(APP_DIR),
        host="0.0.0.0",
        port=8700,
        reload=True,
    )
