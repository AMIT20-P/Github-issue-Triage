# server/app.py
# Server-mode entry point for multi-mode deployment.
# Imports and re-exports the FastAPI application from the root app module.

from app import app, main  # noqa: F401

if __name__ == "__main__":
    main()
