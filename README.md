# Python Script Executor API

## Project Overview
This project is a Flask-based API service that enables secure execution of arbitrary Python scripts. It allows users to upload a Python script with a `main()` function, and returns the function's JSON output. The service ensures security by using `nsjail` to sandbox the execution environment, preventing unauthorized system access.

## Features
* **Secure Execution**: Scripts are executed in a restricted `nsjail` environment, limiting system access and mitigating risks associated with arbitrary code execution.
* **Error Handling**: Validates that uploaded scripts contain a `main()` function and that the function's output is JSON-compatible. Errors are returned for missing `main()` or invalid output formats.
* **Cloud Deployment**: Easily deployable on Google Cloud Run, making the API accessible as a cloud service.


## Technical Details
* **API Endpoint**: Accepts POST requests with the Python script provided in JSON format. Executes the `main()` function and returns its JSON result or an error message.
* **Dockerized**: Built with `python:3.9-slim-buster` for an efficient and lightweight Docker image.
* **Google Cloud Run Compatible**: Deployable on Google Cloud Run using the second-generation runtime environment for enhanced compatibility with `nsjail`.
* **The link of the app**: [Google cloud url][https://python-script-executor-997189946535.us-central1.run.app/]

## Deployment Instructions
* **Local Testing**: Build and run the Docker image locally using `docker build` and `docker run` commands.
* **Cloud Deployment**: Deploy the Docker image to Google Cloud Run, specifying the second-generation runtime environment for full compatibility. Upon deployment, Google Cloud Run provides a public URL to access the API.

## Requirements
* Python 3.9+
* Docker
* Google Cloud SDK (for deployment)

## Estimated Setup Time
The estimated setup and deployment time for this project is approximately **10 hours**.
