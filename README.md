# braintrust-dev-project-export

This is a Python script to conveniently download all experiments and datasets in a
project into a local directory as CSVs.

We'll use this example project, [text2sql-test-project](https://www.braintrust.dev/app/ben-test-org/p/text2sql-test-project/experiments?ye=metric|duration,metric|llm_duration,metric|prompt_tokens,metric|completion_tokens,metric|total_tokens), to demonstrate the script.

## Usage

_First make sure to complete [Requirements](#requirements) & [Installation](#installation) steps._

```bash
# Show available commands
bt-import --help

# Download all experiments and datasets
bt-import download

# Download from a specific project
bt-import download --project PROJECT_ID

# List all available projects
bt-import list-projects
```

## Installation

1. Complete [Requirements](#requirements)
2. Run `make install`

## Requirements

* Have pyenv installed on your machine's local user environment
* Have pre-commit installed on your machine's local user environment
* Clone <https://github.com/salesforce/WikiSQL> to a sister repo on the user's local machine

## Assignment

> Write a script that downloads all of the experiments and datasets in a project into a directory as CSVs. Each experiment and dataset should be in its own file. You can find information about Braintrust and the API in our docs.
>
> This prompt is purposely ambiguous, so don't hesitate to ask me and Natty (cc'ed)
> questions.

### Solution

Create a CLI script installable by pipx that downloads all experiments and datasets in a project into a directory as CSVs.

1. Complete the [Cookbook](https://www.braintrust.dev/docs/cookbook) tutorial, [Text2SQL recipe](https://www.braintrust.dev/docs/cookbook/recipes/Text2SQL)

### References

Should you wish to do more reading on the Braintrust API, and other sources that
inspired this script, here are some references:

* <https://www.braintrust.dev/docs/start/eval-sdk>
* <https://www.braintrust.dev/docs/reference/libs/python>
* <https://pypi.org/project/braintrust/>
* <https://ipywidgets.readthedocs.io/en/stable/user_install.html>
* <https://stackoverflow.com/questions/60971502/python-poetry-how-to-install-optional-dependencies>
