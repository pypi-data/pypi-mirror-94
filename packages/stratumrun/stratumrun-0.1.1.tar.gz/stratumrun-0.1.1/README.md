# Stratum Run Library for Python3

## Overview

**Stratum Run** is a tool that allows users to quickly execute scripts using in common languages such as Python, Javscript, etc.

Check out https://stratumcloud.io for more information on Stratum.

## Python Library

This Python module for **Stratum Run** allows you to run scripts in an isolated environment, so hackers can't mess with your environment, secrets, or system.

## Usage

```py
from stratumrun import StratumRun

# Create a Stratum run instance with your API key
s = StratumRun(key="API KEY")

# Run your command and wait for a response
response = s.run("print(\"hello world\")", language="python3", timeout=30)
print(response.stdout)

# To start a command where you don't need to wait for the response, you can call the start function. Returns a job ID string
job = s.start("time.sleep(10)", language="python3", timeout=11)
print(job)

# To get the response, call the get function with the job ID
import time
time.sleep(15)

response = s.get(job)
print(response.stdout)

```

## The `Response` Object

The `run` call returns a `Response` object with the following fields:
* stdout
* stderr
* duration
* metrics
* status