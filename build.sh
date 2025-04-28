#!/usr/bin/env bash
# exit on error
set -o errexit

# Print environment for debugging
echo "Build script starting"
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Install dependencies
echo "Installing dependencies from requirements-render.txt"
pip install -r requirements-render.txt

# Set RENDER environment variable
export RENDER=true

# Create directories for Flask templates and static files
echo "Setting up template directories..."
mkdir -p /opt/render/project/src/templates
mkdir -p /opt/render/project/src/static/css
mkdir -p /opt/render/project/src/static/js

# Copy templates to the app directory
echo "Copying templates..."
cp -r templates/* /opt/render/project/src/templates/
cp -r static/* /opt/render/project/src/static/

# Update Procfile to use direct.py explicitly
echo "Updating Procfile to use direct.py"
echo "web: gunicorn direct:app" > Procfile

# Ensure direct.py is the main application file
echo "Setting up direct.py as the main application"
cp direct.py /opt/render/project/src/app.py

# List template files for verification
echo "Verifying template files were copied:"
ls -la /opt/render/project/src/templates
echo "Verifying static files were copied:"
ls -la /opt/render/project/src/static/css
ls -la /opt/render/project/src/static/js

# Success!
echo "Build completed successfully"