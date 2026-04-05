# server/app.py
# Server-mode entry point for multi-mode deployment.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: F401


def main():
    """Main entry point for server-mode deployment."""
    import uvicorn
    uvicorn.run(
        "app:app",
        host   = "0.0.0.0",
        port   = int(os.getenv("PORT", "7860")),
        reload = False,
    )


if __name__ == "__main__":
    main()
