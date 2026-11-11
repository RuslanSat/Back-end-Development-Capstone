#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py shell -c "from concert.models import Concert; from datetime import date; Concert.objects.get_or_create(concert_name='Coachella 2023', defaults={'duration':72,'city':'Indio, California','date':date(2023,4,14)})"
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput || true
fi
exec "$@"
