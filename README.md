# Djirection band website

Completed Django capstone based on the IBM Skills Network template.

## Run locally

```shell
python -m venv .venv
# Activate the virtual environment for your shell.
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/. The site provides Home, Songs with lyrics modals, Photos, sign-up, login/logout, and authenticated concert attendance. Concerts are managed in `/admin/`.

The initial exercises use the single song and photo specified in the lab. Set `SONGS_URL` and `PHOTOS_URL` to connect the deployed microservices. The views then fetch `/song` and `/picture` from those services; no fallback data is used for configured endpoints.

## Verification

```shell
python manage.py check
python manage.py test concert -v 2
```

The tests cover public pages, secure password storage, duplicate sign-up handling, login/logout, authenticated concert access, and RSVP persistence.

## Container and Kubernetes

```shell
docker build . -t djangoserver
docker tag djangoserver us.icr.io/sn-labs-u241983/djangoserver:1
docker push us.icr.io/sn-labs-u241983/djangoserver:1
kubectl apply -f deployment.yml
kubectl rollout status deployment/djangoserver
kubectl port-forward deployment/djangoserver 8000:8000
```

The Docker image uses Python 3.12 with Django 5.2. The entrypoint applies migrations and seeds the sample Coachella concert. A superuser is created only when the standard `DJANGO_SUPERUSER_*` environment variables are supplied. Passwords are not committed. SQLite is appropriate for this single-replica lab; a production deployment should use a persistent database and a production WSGI server.
