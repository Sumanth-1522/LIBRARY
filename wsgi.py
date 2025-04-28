"""WSGI entry point for the application.

This is used by Render.com and other hosting platforms.
"""

from direct import app as application

# This is needed for Render.com
app = application