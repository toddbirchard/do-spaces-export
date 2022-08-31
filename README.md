# Digital Ocean Spaces Export

![Python](https://img.shields.io/badge/Python-^3.9-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Boto3](https://img.shields.io/badge/Boto3-^v1.24.0-blue.svg?longCache=true&logo=fastapi&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/do-spaces-export.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/do-spaces-extract/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/do-spaces-export.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/do-spaces-extract/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/do-spaces-export.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/do-spaces-extract/network)

Download all files from a Digital Ocean bucket.

## Getting Started

### Configuration

Populate the values in **.env.example** with your values and rename this file to **.env**:

* `DO_STORAGE_REGION_NAME`: Region name of your DO space (ie: `nyc3`)
* `DO_STORAGE_SPACE_URL`: Public URL of your DO space.
* `DO_STORAGE_KEY_ID`: Digital Ocean API key ID.
* `DO_STORAGE_KEY_SECRET`:  Digital Ocean API key secret.
* `DO_STORAGE_BUCKET_NAME`: Local directory to download files to from space.

### Installation

Get up and running with `make deploy`:

```shell
$ git clone https://github.com/toddbirchard/do-spaces-export.git
$ cd do-spaces-export
$ make deploy
``` 