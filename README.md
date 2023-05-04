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
- get the changes between the two target versions and/or a diff'ed version, or both

If any changes found between the two target versions, add a entry of the diff report including all fields above.

## Example output for report entry

```json
{
    "key": "2afbc5cfc92d36d81610cedcc854778e", 
    "source_text": "Bats send out sound waves and listen for the echoes to help them\xa0locate objects and food.", 
    "target_orig": "Les chauves-souris émettent des ondes sonores puis en écoutent les échos pour pouvoir localiser des objets ou de la nourriture.", 
    "target_edit": "Les chauves-souris envoient des ondes sonores puis en écoutent les échos pour pouvoir localiser des objets ou de la nourriture.", 
    "dmp_diff": [(0, "Les chauves-souris "), (-1, "ém"), (0, "e"), (-1, "tt"), (1, "nvoi"), (0, "ent des ondes sonores puis en écoutent les échos pour pouvoir localiser des objets ou de la nourriture.")], 
    "html_diff": "Les chauves-souris <del>émettent</del><ins>envoient</ins> des ondes sonores puis en écoutent les échos pour pouvoir localiser des objets ou de la nourriture.", 
    "file": "PISA_2025FT_SCI_CACERS001-BatEcholocation.xml"
}
```

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

Activate the virtual environment (before every timem you run the script)

```
source venv/bin/activate
```

You may exit the virtual environment when you're done running the code:

```
deactivate
```
