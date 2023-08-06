## Introduction

`cyjax-vectra-integration` is an integration for [Vectra](https://www.vectra.ai) and it can be used to ingest 
indicators of compromise.

The library is available on [Python Package Index](http://pypi.python.org/pypi/cyjax-vectra-integration).

## Install

You can install the `cyjax-vectra-integration` library with pip:

```shell
pip install --user cyjax-vectra-integration
```

## Configuration

To set the integration up, you have to provide:

- Cyjax API key: the API key for the Cyjax platform API.
- Vectra FQDN: the fully qualified domain name to Vectra Brain.
- Vectra API key: the API key for Vectra REST API.
- Vectra threat feed ID: the threat feed ID where to save indicators.

Then please run:

```shell
$HOME/.local/bin/cyjax-vectra-integration --setup

=== Vectra integration for Cyjax Threat Intelligence platform ===

Please provide the Cyjax API key: g5d9fig0db5b6b7022d3a5d3c93883g4
Please provide the Vectra FQDN: brain.vectra-fqdn.com
Please provide the Vectra API key: X2QrvRBwblBbd9nGa8Z2aJHDYZFoVFFiAadolPUU
Please provide the Vectra Threat feed ID: 20
```

## Run

Please set a cronjob up to run the Vectra integration every hour:

```shell
crontab -e
0 * * * * $HOME/.local/bin/cyjax-vectra-integration
```

## Uninstall

To remove the Vectra integration, please run:

```shell
pip uninstall cyjax-vectra-integration
rm $HOME/.config/ccyjax_vectra_integration.json
```
