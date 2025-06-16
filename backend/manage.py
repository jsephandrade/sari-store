import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sari_store.settings')
    from django.core.management import execute_from_command_line

    # Automatically apply pending migrations whenever the development server is
    # started. This avoids "no such table" errors on a fresh setup.
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])

    execute_from_command_line(sys.argv)
