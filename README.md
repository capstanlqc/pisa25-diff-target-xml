# PISA 2025 -- diff tool

This is a draft proposal for a diff utility to compare the output of different steps in a translation workflow.

The Python code included can be used as pseudo-code to understand the proposed logic but should be working well when executed.

## To run the backend code

To running the code, you need to clone the repository, create a virtual environment and install dependencies in it. That only needs to be done once. 

When your virtual environment is created, when the you can simply activate it before running the code (and dectivate it when it's no longer needed).

### Steps: 

Clone this repo and change directory to it

```
gh repo clone capstanlqc/pisa25-diff-target-xml
cd pisa25-diff-target-xml
```

Install a virtual environment in the root folder of the repo (only once)

```
python -m venv venv
```

Activate the virtual environment

```
source venv/bin/activate
```

This is needed every time you need to run the code.

Install dependencies (only once)

```
pip install -r requirements.txt
```

Now you can run the code:

```
python3 code/main.py
```

You may exit the virtual environment when you're done running the code:

```
deactivate
```
