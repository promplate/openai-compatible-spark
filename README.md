# Spark -> OpenAI API wrapper

This server wraps Spark's API as OpenAI's

## Install

Install `pdm` and then install dependencies

```shell
pip install pdm
pdm install
```

## Deploy

You need to set 3 environment variables:

```properties
APPID=
APISecret=
APIKEY=
```

Start the development server:

```shell
pdm dev
```

You can use `Docker` to deploy too. After setuping the environment variables, run:

```shell
docker build -t spark2o .
docker run -p 9040:9040 spark2o
```
