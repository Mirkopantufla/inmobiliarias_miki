#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

python manage.py makemigrations app

python manage.py migrate

python manage.py loaddata 'tipo_usuario.json'
python manage.py loaddata 'tipo_inmueble.json'
python manage.py loaddata 'tipo_imagen.json'
python manage.py loaddata 'regiones.json'
python manage.py loaddata 'comunas.json'
python manage.py loaddata 'users.json'
python manage.py loaddata 'profiles.json'
python manage.py loaddata 'inmuebles.json'