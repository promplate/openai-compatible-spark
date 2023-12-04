FROM python:3.12-slim

WORKDIR /

COPY /pyproject.toml /

RUN pip3 install pdm && pdm install --prod && pdm venv activate > /activate-command.txt && \
    pip3 freeze | xargs pip3 uninstall -y && rm ~/.cache -rf && touch .env

EXPOSE 9040

COPY . .

CMD /bin/bash -c "$(cat /activate-command.txt) && python3 -O -m uvicorn server:app --host 0.0.0.0 --port 9040"