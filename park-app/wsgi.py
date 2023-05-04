#!/usr/bin/env python
# Entry point for the application in production environment
from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
