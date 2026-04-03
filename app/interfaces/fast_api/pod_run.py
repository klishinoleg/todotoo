from pathlib import Path
import sys

import uvicorn

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from interfaces.fast_api.main import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
