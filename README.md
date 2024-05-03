<p align="center">
  <a href="https://mqt.readthedocs.io">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/mqt_light.png" width="60%">
     <img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/mqt_dark.png" width="60%">
   </picture>
  </a>
</p>

# MQT as a Service @ PlanQK

This repository contains services for the [PlanQK Platform](https://platform.planqk.de) based on the [_Munich Quantum Toolkit (MQT)_](https://mqt.readthedocs.io/) that is developed by the [Chair for Design Automation](https://www.cda.cit.tum.de/) at the [Technical University of Munich](https://www.tum.de/).
Currently, the following services are available:

- [MQT DDSIM](https://github.com/cda-tum/mqt-ddsim): A Tool for Classical Quantum Circuit Simulation based on Decision Diagrams.
- [MQT QMAP](https://github.com/cda-tum/mqt-qmap): A Tool for Quantum Circuit Mapping.
- [MQT QCEC](https://github.com/cda-tum/mqt-qcec): A Tool for Quantum Circuit Equivalence Checking.
- [MQT Bench](https://github.com/cda-tum/mqt-bench): A tool for Benchmarking Software and Design Automation Tools for Quantum Computing.

For a full list of tools and libraries available as part of the MQT, please visit the [MQT website](https://mqt.readthedocs.io/).

<p align="center">
  <a href="https://mqt.readthedocs.io/">
  <img width=30% src="https://img.shields.io/badge/MQT@ReadTheDocs-blue?style=for-the-badge&logo=read%20the%20docs" alt="Documentation" />
  </a>
</p>

> [!NOTE]\
> All services are still experimental and under development. Expect breaking changes.

## Usage

The fist goal is to be able to run the `src` directory as a Python module with the code inside `program.py`.

We recommend building your service from within a dedicated and fresh Conda environment to install and track all required packages from the start.
For this reason, the template already contains an `environment.yml` file from which a fresh environment can be created:

> **HINT:**
> As an alternative to Conda, you may use the `requirements.txt` file to create a virtual environment with the tooling of your choice.

```bash
conda env create -f environment.yml
conda activate mqt-<SERVICE_NAME>
python3 -m src
```

## Run the project using Docker

You may utilize Docker to run your code locally and test your current implementation.
In general, by following the next steps you replicate the steps done by the PlanQK platform, which is a way to verify your service in an early stage.

### Build the Docker image

```bash
docker pull ghcr.io/planqk/job-template:latest-base-1.0.0
docker build -t mqt-<SERVICE_NAME> .

# or (for Apple M1 chips)
docker buildx build -o type=docker --platform "linux/amd64" --tag mqt-<SERVICE_NAME> .
```

### Start the Docker container

In case, you do not use any input data or parameters that need to be passed into the container, you may run the container with the following command:

```bash
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  mqt-<SERVICE_NAME>
```

However, to pass the `"data"` and `"params"` attributes as JSON-serialized files into the container, you either mount it in the form of separate files (recommended) or pass it as environment variables (base64 encoded).

To use the [`data.json`](input/data.json) and [`params.json`](input/params.json) from the [`input`](input) directory, you could execute the following command:

```bash
PROJECT_ROOT=(`pwd`)
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  -v $PROJECT_ROOT/input:/var/input \
  mqt-<SERVICE_NAME>
```

If the service executed successfully, you should see something like `Job:ResulsResponse:` followed by the output you defined for your service.
Otherwise, if you see `Job:ErrorResponse`: Bad news, something went wrong.
However, the details of the response hopefully give you a clue what the problem was.

---

## Acknowledgements

The Munich Quantum Toolkit has been supported by the European
Research Council (ERC) under the European Union's Horizon 2020 research and innovation program (grant agreement
No. 101001318), the Bavarian State Ministry for Science and Arts through the Distinguished Professorship Program, as well as the
Munich Quantum Valley, which is supported by the Bavarian state government with funds from the Hightech Agenda Bayern Plus.

<p align="center">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/tum_dark.svg" width="28%">
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/tum_light.svg" width="28%">
</picture>
<picture>
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/logo-bavaria.svg" width="16%">
</picture>
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/erc_dark.svg" width="24%">
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/erc_light.svg" width="24%">
</picture>
<picture>
<img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/logo-mqv.svg" width="28%">
</picture>
</p>
