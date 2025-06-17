# XSS_Polyglot_with_DE
 Evolution complete : XSS Polyglot Optimization through DE Algorithm

This repo contains the results of research on generating XSS Polyglot using the DE algorithm.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Cross-Site Scripting (XSS) is a common web vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users. XSS polyglots are unique payloads that can execute in multiple contexts. In particular, XSS Polyglot is a payload that can be used to detect blind XSS, and can be optimized through the DE algorithm to generate a polyglot of the user's desired length.

## Features

- **Automated Polyglot Generation**: Generate XSS polyglot payloads with customizable parameters.
- **Context Analysis**: Analyze and adapt payloads for different execution contexts.

## Installation
### Setup [BXSS](https://github.com/polyxss/bxss) Testbed
This project utilizes the testbed from the [Dancer in the Dark](https://github.com/polyxss/bxss) repository for testing XSS polyglots. You need to install the testbed from the bxss repository and start the server before using this project.
To get started with the project, clone the repository and install the necessary dependencies.

```
git clone https://github.com/wodn1478/XSS_Polyglot_with_DE.git
cd XSS_Polyglot_with_DE

```
Install the required Python libraries:

```
pip install numpy selenium webdriver-manager requests DateTime
```

Start the BXSS testbed and ensure that it is reachable at
`http://localhost:8080` before running the scripts. The scripts rely on this
server to evaluate generated payloads.

## Usage

The repository includes several helper scripts. In most cases you can simply
run them with Python:

```bash
python Differential_Evolution_Polyglot_v1.py
```

or

```bash
python Differential_Evolution_Polyglot_v2.py
```

These scripts will use Selenium to automatically send generated payloads to the
BXSS testbed and evolve them using the Differential Evolution algorithm. At the
end of the run a `best_xss_payload_*.txt` file is written containing the
high‑scoring polyglots.

### Encoding utilities

`StringToCodes.py` converts a given payload to multiple encoded
representations. Provide the path to a file containing your payload as the first
argument:

```bash
python StringToCodes.py payload.txt
```

### Testing against Public Firing Range

`Gfr_test.py` contains examples of how to automatically test a payload against
Google's Public Firing Range. The endpoints list in this script can be adjusted
to experiment with different XSS sinks.
