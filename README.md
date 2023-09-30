# vcamp

## Local Setup

- create `.env` file in root directory and populate all environment variables listed below. Do NOT commit this file

```toml
# conf
SECRET_KEY=<secret_key>
DEBUG=<debug>
ALLOWED_HOSTS=<allowed_hosts>

# auth
JWT_SIGNING_KEY=<key>

# database
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
POSTGRES_DB=<db_name>
POSTGRES_HOST=<db_host>
POSTGRES_PORT=<db_port>

# eden ai
EDENAI_API_KEY=<edenai_key>

# aws-s3-bucket-configuration
AWS_ACCESS_KEY_ID=<access_key>
AWS_SECRET_ACCESS_KEY=<secret_key>
AWS_STORAGE_BUCKET_NAME=<s3_bucket>
AWS_S3_REGION_NAME=<bucket_region>

#celery
CELERY_BROKER_URL=<redis_url>

# papertrail logs configuration
PAPERTRAIL_HOST=<papertrail_host>
PAPERTRAIL_PORT=<papertrail_port>
```

- Run web service

```commandline
sudo docker-compose up --build
```

- Create an admin user

```commandline
sudo docker-compose run web python manage.py createsuperuser --email admin@example.com --username admin
```

```commandline
sudo docker exec -it <container_id> python manage.py createsuperuser --email admin@example.com --username admin
```

## DRF

- Go to `/api/` to check all available rest APIs
- Login with admin or any other user to try out API
