![logo](https://raw.githubusercontent.com/Asconius/media/master/predictor/logo.png)

[![Python application](https://github.com/Asconius/predictor/workflows/Python%20application/badge.svg)](https://github.com/Asconius/predictor/actions?query=workflow%3A%22Python+application%22)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Asconius_predictor&metric=alert_status)](https://sonarcloud.io/dashboard?id=Asconius_predictor)
[![codecov](https://codecov.io/gh/Asconius/predictor/branch/main/graph/badge.svg?token=7T01ZCVKNP)](https://codecov.io/gh/Asconius/predictor)

# Predictor

Timeseries forecasting for stock prediction.

## Installation

### Enviroment Variables

The following command must be used to insert the [Alpha Vantage API key][cb956311] into the environment variables in
Windows:

```batch
setx ALPHAVANTAGE_API_KEY "API key" /m
```

### Docker

The Docker image can be created with the following command:

```
docker build --build-arg alphavantage_api_key=${ALPHAVANTAGE_API_KEY} -t predictor_image .
```

The Docker container can be started with the following command:

```
docker run -d --name predictor_container predictor_image
```

### Packaging

The package can be generated with the following command:

```
python setup.py sdist bdist_wheel
```

The package can be installed with the following command:

```
python setup.py install
```

[cb956311]: https://www.alphavantage.co/support/#api-key "Alpha Vantage API key"