#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("render_builder")

def main():
    """
    Explicitly copy template and static files to the correct location for Render.
    This script should be run as part of the build process.
    """
    logger.info("Starting Render build script")
    
    # Get current directory
    BASE_DIR = Path.cwd()
    logger.info(f"Working directory: {BASE_DIR}")
    
    # Define target directories in Render environment
    target_root = Path('/opt/render/project/src')
    target_templates = target_root / 'templates'
    target_static = target_root / 'static'
    
    # Create target directories
    os.makedirs(target_templates, exist_ok=True)
    os.makedirs(target_static / 'css', exist_ok=True)
    os.makedirs(target_static / 'js', exist_ok=True)
    
    logger.info(f"Created target directories at {target_templates} and {target_static}")
    
    # Source directories
    source_templates = BASE_DIR / 'templates'
    source_static = BASE_DIR / 'static'
    
    # Copy template files
    if source_templates.exists():
        logger.info(f"Copying templates from {source_templates}")
        for file in source_templates.glob('*.html'):
            target_file = target_templates / file.name
            shutil.copy2(file, target_file)
            logger.info(f"Copied {file.name} to {target_file}")
    else:
        logger.error(f"Template directory not found at {source_templates}")
        return 1
    
    # Copy static files
    if source_static.exists():
        # Copy CSS files
        css_dir = source_static / 'css'
        if css_dir.exists():
            for file in css_dir.glob('*.*'):
                target_file = target_static / 'css' / file.name
                shutil.copy2(file, target_file)
                logger.info(f"Copied CSS file {file.name}")
        
        # Copy JS files
        js_dir = source_static / 'js'
        if js_dir.exists():
            for file in js_dir.glob('*.*'):
                target_file = target_static / 'js' / file.name
                shutil.copy2(file, target_file)
                logger.info(f"Copied JS file {file.name}")
    else:
        logger.error(f"Static directory not found at {source_static}")
        return 1
    
    # Verify files were copied
    if not list(target_templates.glob('*.html')):
        logger.error("No template files found after copying")
        return 1
    
    logger.info("Build process completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())