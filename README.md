# PISA 2025 -- diff tool

This is a draft proposal for a diff utility to compare the output of different steps in a translation workflow.

The Python code included can be used as pseudo-code to understand the proposed logic but should be working well when executed.

## Business logic in a nutshell

Provided the following as input: 

- a folder containing the source files (e.g. `source` dir in the common repo)
- a folder containing the original version of the target files (e.g. `target` dir in project for step *n*)
- a folder containing the edited version of the target files (e.g. `target` dir in project for step *n+1*)

For every file: 

- grab all keys from the source version

For every key: 

- get the source text associated with the key
- get the original target text associated with the they, if found
- get the edited target text associated with the key, if found
- get the changes between the two target versions or a diff'ed version, or both

If any changes found between the two target versions, add a entry of the diff report including all fields above.

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
details 
```

You may exit the virtual environment when you're done running the code:

```
deactivate
```
