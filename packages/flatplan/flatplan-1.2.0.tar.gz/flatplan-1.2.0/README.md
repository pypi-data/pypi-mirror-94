# Flatplan


![](https://github.com/egonbraun/flatplan/workflows/CI/badge.svg)

Flatplan is a command line tool that can be used to *flatten* the resources and providers found inside a terraform
plan or state.

You can obtain a JSON version of the plan or state by running:

```bash
terraform plan -out=planfile
terraform show -json planfile > plan.json
```

Now, we can feed our exported JSON plan to flatplan:

```bash
flatplan --path=plan.json --output=flattened_plan.json --debug
```

The problem we are trying to solve with flatplan is that, when you export the plan or state to JSON the resources might
be in different locations which makes it hard for other tools to find them. Therefore, flatplan will extract all
resources and providers for you and return a much simpler JSON structure.

For example, let's say we have a complex terraform project that uses many modules and submodules. When we create the
plan file for this project and then export it to JSON we might end up with something like this:

```json
{
    "planned_values": {
        "root_module": {
            "resources": [
                "... a lot of resources here ..."
            ],
            "child_modules": [{
                "resources": [
                    "... a lot of resources here ..."
                ],
                "child_modules": [{
                    "resources": [
                        "... a lot of resources here ..."
                    ],
                    "child_modules": [{
                        "... and so on ...": "..."
                    }]
                }]
            }, {
                "resources": [
                    "... a lot of resources here ..."
                ],
                "child_modules": [{
                    "resources": [
                        "... a lot of resources here ..."
                    ],
                    "child_modules": [{
                        "... and so on ...": "..."
                    }]
                }]
            }]
        }
    },
  
    "... some other things here ...": [],
  
    "configuration": {
        "provider_config": {
            "aws": {
                "name": "aws",
                "expressions": {
                    "region": {
                        "constant_value": "us-east-1"
                    }
                }
            }
        }
    }
}
```

If you are interested in this format you can check [this](https://www.terraform.io/docs/internals/json-format.html)
Terraform documentation.

As you can see this recursive nature of the plan can get quite ugly if you use a lot of modules and submodules. After,
flatplan process this file we will get:

```json
{
    "resources": [ "... all resources here ..." ],
    "providers": [ "... all providers here ..." ]
}
```

This makes it easy for tools like Open Policy Agent to process our file since it has no way to recursively traverse a
raw terraform plan.

## Install


If you use pip:

```bash
pip install flatplan
```

If you use pipx:

```bash
pipx install flatplan
```

## Usage

Flatplan accepts the following command line parameters:

`--debug` Sets log level to debug, default: False.

`--output="path"` Writes flattened plan to the specified path, default: STDOUT.

`--path="path"` Reads JSON plan from the specified path, default: STDIN.

`--remove="tag=value"` Removes the resources that contain a certain tag, default: empty

`--state` Whether the file passed in the path option is a state file instead of a plan file, default: false

Examples:

```bash
flatplan --debug --output=flattened.json --path=plan.json --remove="remove=true"
```

Alternatively, if you want to flatten a state:

```bash
flatplan --debug --output=flattened.json --path=state.json --remove="remove=true" --state
```
