# Dockerfile
# Packages the entire project into a Docker container
# Hugging Face Spaces reads this file and builds the container automatically
#
# WHAT IS DOCKER?
#   A Docker container = your code + Python + all libraries sealed in one box
#   Anyone can run this box with one command — no setup needed
#
# HOW HUGGING FACE USES THIS:
#   You push code to HF Spaces → HF reads Dockerfile → builds container → runs it
#   Your environment is now live at a public URL!

# ── Step 1: Start with Python 3.11 slim base image ──
# "slim" = minimal version, smaller file size
FROM python:3.11-slim

# ── Step 2: Set working directory inside container ──
# All files will live in /app inside the container
WORKDIR /app

# ── Step 3: Copy requirements.txt FIRST (for Docker cache) ──
# Docker caches each step. If requirements.txt hasn't changed,
# it reuses the cached pip install from last time → much faster builds
COPY requirements.txt .

# ── Step 4: Install all Python dependencies ──
# This runs INSIDE the container during build time
RUN pip install --no-cache-dir -r requirements.txt

# ── Step 5: Copy all project files into the container ──
COPY . .

# ── Step 6: Tell Docker which port the app uses ──
# Hugging Face Spaces REQUIRES port 7860
EXPOSE 7860

# ── Step 7: The command to run when container starts ──
# uvicorn = the ASGI server that runs FastAPI apps
# app:app = file "app.py", object "app"
# --host 0.0.0.0 = accept connections from anywhere (not just localhost)
# --port 7860    = listen on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
