# metalmetrics

[![Actions Status](https://github.com/craftslab/metalmetrics/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/craftslab/metalmetrics/actions?query=workflow%3ACI)
[![Docker](https://img.shields.io/docker/pulls/craftslab/metalmetrics)](https://hub.docker.com/r/craftslab/metalmetrics)
[![License](https://img.shields.io/github/license/craftslab/metalmetrics.svg?color=brightgreen)](https://github.com/craftslab/metalmetrics/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/metalmetrics.svg?color=brightgreen)](https://pypi.org/project/metalmetrics)
[![Tag](https://img.shields.io/github/tag/craftslab/metalmetrics.svg?color=brightgreen)](https://github.com/craftslab/metalmetrics/tags)



## Introduction

*metalmetrics* is a worker of *[metalflow](https://github.com/craftslab/metalflow/)* written in Python.



## Prerequisites

- Python >= 3.7



## Run

- **Local mode**

```bash
git clone https://github.com/craftslab/metalmetrics.git

cd metalmetrics
pip install -Ur requirements.txt
python metrics.py --config-file="config.yml" --inxi-file="inxi" --output-file="output.json"
```



- **Service mode**

```bash
git clone https://github.com/craftslab/metalmetrics.git

cd metalmetrics
pip install -Ur requirements.txt
python metrics.py --config-file="config.yml" --inxi-file="inxi" --listen-url="127.0.0.1:9090"
```



## Docker

- **Local mode**

```bash
git clone https://github.com/craftslab/metalmetrics.git

cd metalmetrics
docker build --no-cache -f Dockerfile -t craftslab/metalmetrics:latest .
docker run -it -v /tmp:/tmp craftslab/metalmetrics:latest ./metalmetrics --config-file="config.yml" --output-file="/tmp/output.json"
```



- **Service mode**

```bash
git clone https://github.com/craftslab/metalmetrics.git

cd metalmetrics
docker build --no-cache -f Dockerfile -t craftslab/metalmetrics:latest .
docker run -it -p 9090:9090 craftslab/metalmetrics:latest ./metalmetrics --config-file="config.yml" --listen-url="127.0.0.1:9090"
```



## Usage

```
usage: metrics.py [-h] --config-file CONFIG_FILE [--inxi-file INXI_FILE]
                  [--listen-url LISTEN_URL | --output-file OUTPUT_FILE] [-v]

Metal Metrics

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        config file (.yml)
  --inxi-file INXI_FILE
                        inxi file (/path/to/inxi)
  --listen-url LISTEN_URL
                        listen url (host:port)
  --output-file OUTPUT_FILE
                        output file (.json|.txt|.xlsx)
  -v, --version         show program's version number and exit
```



## Settings

*metalmetrics* parameters can be set in the directory [config](https://github.com/craftslab/metalmetrics/blob/master/metalmetrics/config).

An example of configuration in [config.yml](https://github.com/craftslab/metalmetrics/blob/master/metalmetrics/config/config.yml):

```yaml
apiVersion: v1
kind: worker
metadata:
  name: metalmetrics
spec:
  bare:
    - cpu
    - disk
    - io
    - ip
    - kernel
    - mac
    - network
    - os
    - ram
    - system
  container:
  kubernetes:
```



## Design

![design](design.png)



## License

Project License can be found [here](LICENSE).



## Reference

- [gRPC](https://grpc.io/docs/languages/python/)
- [health-check-script](https://github.com/SimplyLinuxFAQ/health-check-script)
- [inxi](https://github.com/smxi/inxi)
- [python-diamond](https://github.com/python-diamond/Diamond)
- [sysperf](https://github.com/iandk/sysperf)
