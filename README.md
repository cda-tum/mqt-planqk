# mqt-ddsim

This is a PlanQK Service template for Python.
With only a few more steps until your quantum code is ready to be deployed as a PlanQK Service!

## Project structure

Your code must be structured in a (not too) specific way.
After generating/extracting it, you should find the following structure:

```
.
├── Dockerfile
├── openapi-spec.yml
├── environment.yml
├── requirements.txt
├── input
│   └── ...
└── src
    ├── __init__.py
    ├── __main__.py
    ├── libs
    │   ├── __init__.py
    │   ├── return_objects.py
    │   └── ...
    └── program.py
```

The most important method is the `run` method inside `program.py`.
It provides access to a `data` dictionary and a `params` dictionary, representing the user input through the exposed service API.
The PlanQK Platform ensures that the input provided via the Service API in the form of `{ "data": <data>, "params": <params> }` is provided to your code at runtime.

> **IMPORTANT:**
> Do not rename either the `src` folder, the `program.py` package, as well as the `run` method inside it.
> These are fixed entry points for your service.
> Changing their names will result in a malfunctioning service.

## What does the starter template do?

The starter template shows how to use Qiskit to run a simple quantum circuit on Qiskit's Aer simulator.

The logic implements a simple quantum circuit to generate a random number.
As input, you can the number of bits (`n_bits`), which defines the range of random numbers between `0` and `2^n_bits - 1` (see [data.json](./input/data.json)).
Further, it provides a flag to specify whether to use a simulator or a real quantum computer, configurable through parameters (see [params.json](./input/params.json)).

If the `src` folder is executed as a Python module, the `__main__.py` is executed.
It loads the input data from the `input` folder and calls the `run()` method of the `program.py` file.
This is helpful for local testing.

## Usage

The fist goal is to be able to run the `src` directory as a Python module with the code inside `program.py`.

We recommend building your service from within a dedicated and fresh Conda environment to install and track all required packages from the start.
For this reason, the template already contains an `environment.yml` file from which a fresh environment can be created:

> **HINT:**
> As an alternative to Conda, you may use the `requirements.txt` file to create a virtual environment with the tooling of your choice.

```bash
conda env create -f environment.yml
conda activate mqt-ddsim
python3 -m src
```

## Extending the coding template

The most important method, which takes the user input and generates the output of interest is the `run()` method inside `program.py`.
You may adapt and extend the code inside this method to your needs.
If you have written packages by yourself, which are required for your service, you can simply put them into the `libs` folder and import them via relative imports into your program.

Any required python package (like `numpy`, `pandas`, ...) must be mentioned within, you guessed it, the `environment.yml` with their version number in the pip-installation format (e.g. `numpy==1.19.0`).
It is important to define your dependencies in the `environment.yml` file as this file is used later by the PlanQK Platform at runtime.
For development, you may use the `requirements.txt` file and a virtual environment tooling of your choice.
Once you've installed your dependencies, you can import these packages within any Python file needed.

> **IMPORTANT:**
> Do not rename either the `src` folder, the `program.py` package, as well as the `run()`-method inside `program.py`.
> These are fixed entry points for the service.
> Changing their names will result in a malfunctioning service.

From the start, you should be able to run `python3 -m src` from within the project folder.
This will execute the `__main__`-method inside the `src` folder.
Locally, you can test your code with a JSON-conform input format that gets imported within the `__main__`-method.
You can use the files in the `input` folder to provide input data and parameters for local testing.
However, you may adjust the `__main__`-method to, for example, load a different set of input data from the `input` folder or to execute the `run()` method with some static test input.

## Run the project using Docker

You may utilize Docker to run your code locally and test your current implementation.
In general, by following the next steps you replicate the steps done by the PlanQK platform, which is a way to verify your service in an early stage.

### Build the Docker image

```bash
docker pull ghcr.io/planqk/job-template:latest-base-1.0.0
docker build -t mqt-ddsim .

# or (for Apple M1 chips)
docker buildx build -o type=docker --platform "linux/amd64" --tag mqt-ddsim .
```

### Start the Docker container

In case, you do not use any input data or parameters that need to be passed into the container, you may run the container with the following command:

```bash
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  mqt-ddsim
```

However, to pass the `"data"` and `"params"` attributes as JSON-serialized files into the container, you either mount it in the form of separate files (recommended) or pass it as environment variables (base64 encoded).

To use the [`data.json`](input/data.json) and [`params.json`](input/params.json) from the [`input`](input) directory, you could execute the following command:

```bash
PROJECT_ROOT=(`pwd`)
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  -v $PROJECT_ROOT/input:/var/input \
  mqt-ddsim
```

> **HINT**
> For GitBash users on Windows, replace
>
> ```bash
> PROJECT_ROOT=(`pwd`)
> ```
>
> with
>
> ```bash
> PROJECT_ROOT=(/`pwd`)
> ```
>
> For Windows command-prompt users, you can use the following command:
>
> ```bash
> docker run -it \
>   -e BASE64_ENCODED=false \
>   -e LOG_LEVEL=DEBUG \
>   -v %cd%/input:/var/input \
>   mqt-ddsim
> ```

> **NOTE:**
> In general, you may mount any JSON-serialized input data file to `/var/input/data.json` and any file containing params to `/var/input/params.json` of the `mqt-ddsim` container.

If the service executed successfully, you should see something like `Job:ResulsResponse:` followed by the output you defined for your service.
Otherwise, if you see `Job:ErrorResponse`: Bad news, something went wrong.
However, the details of the response hopefully give you a clue what the problem was.

Alternatively, you could also pass any input by environment variables.
You can either use command line tools like `base64` or [Base64 Encoder](https://www.base64encode.org) to encode the input.
For example, to create a base64 encoded string of the `"data"` part of the `input.json` file, execute the following:

```bash
base64 -w 0 <<EOF
{"values": [100, 50, 200, 70, 0.69]}
EOF

>> eyJ2YWx1ZXMiOiBbMTAwLCA1MCwgMjAwLCA3MCwgMC42OV19
```

> **NOTE:**
> In general, the maximum default length of environment variables in Linux-based systems is at 128KiB.
> On Windows, the maximum default length is at 32KiB.

To create a base64 encoded string of the `"params"` part, execute the following:

```bash
base64 -w 0 <<EOF
{"round_off": false}
EOF

>> eyJyb3VuZF9vZmYiOiBmYWxzZX0=
```

Then, start the container with the environment variables `DATA_VALUE` and `PARAMS_VALUE` as follows:

```bash
docker run -it \
  -e DATA_VALUE=eyJ2YWx1ZXMiOiBbMTAwLCA1MCwgMjAwLCA3MCwgMC42OV19 \
  -e PARAMS_VALUE=eyJyb3VuZF9vZmYiOiBmYWxzZX0= \
  mqt-ddsim
```

## Next steps

Use `planqk up` to deploy your service to the PlanQK Platform.
Next, you may use `planqk run` to execute your service.
For more information, see the [PlanQK documentation](https://docs.platform.planqk.de/docs/getting-started/quickstart.html).

However, you can also create a PlanQK Service manually via the PlanQK UI at <https://platform.planqk.de>.

> **RECOMMENDED:**
> To offer your service via an API to others, you should also take the time to adapt the `openapi-spec.yml` file, in order to describe your API.
> This will help others to understand how to use your service.
> For more information, see the [PlanQK documentation](https://docs.platform.planqk.de/docs/service-platform/managed-services.html).

### Manual service creation

At last, you must zip (at minimum) the `src` folder and the `environment.yml` file, which will be the file you upload in order to create a PlanQK Service.
**You must not zip the project folder itself but its content.**
Execute the following from within the project folder:

```bash
zip -r planqk.zip src environment.yml
```

Now that you have your service in a zip-file, creating a PlanQK Service via the platform is easy:
From the landing page, go to "[Service Platform > My Services](https://platform.planqk.de/services)".
Here you need to click on `Create Service` in the top right corner.

Fill out the form respectively and import the `planqk.zip` file you created before to create a `Managed Service`.
And there you go.
As soon as you click on "Create Service", the containerization of your code starts and will be deployed on the PlanQK Platform.

As soon as it's finished you will be able to run a PlanQK Job to execute your service.
Further, you may publish it for internal use or into the PlanQK Marketplace to share it with other PlanQK users.
