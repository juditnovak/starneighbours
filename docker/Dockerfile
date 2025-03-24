FROM python:3.11.4

RUN mkdir /home/application
WORKDIR /home/application

RUN apt-get update && \
    apt-get install -y libpq-dev

RUN pip install uv


#
# Dev environment
#

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "starneighbours/main.py"]



#
# Prod environment
#
# COPY pyproject.toml ./
# COPY uv.lock ./
# RUN pip install uv && uv sync --frozen
#
# COPY . .
# CMD ["uv", "run", "fastapi", "run", "--host", "0.0.0.0", "starneighbours/main.py"]
