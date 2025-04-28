import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("Starting WSGI application for Render deployment")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")
logger.info(f"System path: {sys.path}")

# Verify template directories
template_dir = '/opt/render/project/src/templates'
static_dir = '/opt/render/project/src/static'

logger.info(f"Checking template directory: {template_dir}")
if os.path.exists(template_dir):
    logger.info(f"Template directory exists with files: {os.listdir(template_dir)}")
else:
    logger.error(f"Template directory does not exist: {template_dir}")

# Import the Flask app - templates should already be copied by the build process
from app import app as application

# For gunicorn
app = application

# Log routes for debugging
logger.info("Available routes:")
for rule in app.url_map.iter_rules():
    logger.info(f"{rule.endpoint}: {rule}")

if __name__ == "__main__":
    application.run()