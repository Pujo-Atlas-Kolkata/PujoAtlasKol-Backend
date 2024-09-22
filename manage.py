#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Get the port from the .env file or environment variable, default to 8000
    port = config('PORT', default=os.environ.get('PORT', '8000'))

    # Check if the runserver command is being used
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        # If no port is provided in the command, append the port argument
        if len(sys.argv) == 2:
            sys.argv.append('0.0.0.0:' + port)
        # If a port is provided, leave it unchanged

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
