# Use Python 3.11 as a parent image
FROM python:3.11

# Set environment variables
# Django Settings
ENV SECRET_KEY=django-superseceretkey@4^8dve&%jgbk*%!@cjkchty08XTHG)*
ENV DEBUG=False

# Database Credentials
ENV POSTGRES_DB=defaultdb
ENV POSTGRES_USER=avnadmin
ENV POSTGRES_PASSWORD=AVNS_rOQQjEQC4JL9zpMEh-I
ENV POSTGRES_HOST=pg-f6fbbce-saipraveen-6261.a.aivencloud.com
ENV POSTGRES_PORT=17443

# Email Credentials
ENV MAIL_PASSWORD=zjjodzeiwwjafnto
ENV MAIL_USERNAME=saipraveen.dev.acc@gmail.com
ENV MAIL_SERVER=smtp.gmail.com
ENV MAIL_PORT=587
ENV CONTACT_RECEIVER=saipraveenkondapalli@gmail.com
ENV JOB_APPLICATION_RECEIVER=saipraveenkondapalli@gmail.com


ENV BOTO_ACCESS_KEY=96a7c85319532f93d4e09da9051e7e96
ENV BOTO_SECRET_KEY=5ee55866fc9ba163ed50b31c65a5225c0a6c512dceb08c9345942679d1589482
ENV BOTO_BUCKET_NAME=resume
ENV BOTO_ENDPOINT_URL=https://4e3989f550197dead69bd70821c5fc3f.r2.cloudflarestorage.com
ENV SENTRY_DSN=https://e48b2ccf26911214d32ca048ec31837d@o4506573396508672.ingest.sentry.io/4506573402865664
ENV CLOUDINARY_CLOUD_NAME dyqjblbnd
ENV CLOUDINARY_API_KEY 686185378535972
ENV CLOUDINARY_API_SECRET aTVHuFRMWbdLjRPV8YxheQLU9Nc

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]