import os
from app import app  # noqa: F401

# This file is used to run the application
# The app is imported from app.py

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
