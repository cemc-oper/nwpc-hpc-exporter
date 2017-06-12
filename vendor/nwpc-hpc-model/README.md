# nwpc-hpc-model

A collection of models for HPC used in NWPC. Including model for:

* LoadLeveler's job query

## Installation

Download source code from Github releases. Run `python setup.py install` to install.

## Example

The following example use nwpc-hpc-model to extract job id and job owner from a llq -l query.
 
A config json file is used to create query categories.

```json
[
    {
      "id": "llq.id",
      "display_name": "Id",
      "label": "Job Step Id",
      "record_parser_class": "DetailLabelParser",
      "record_parser_arguments": ["Job Step Id"],
      "value_saver_class": "StringSaver",
      "value_saver_arguments": []
    },
    {
      "id": "llq.owner",
      "display_name": "Owner",
      "label": "Owner",
      "record_parser_class": "DetailLabelParser",
      "record_parser_arguments": ["Owner"],
      "value_saver_class": "StringSaver",
      "value_saver_arguments": []
    }
 ]

```

First create some `QueryCategory` according to the config json file.

```python
from nwpc_hpc_model.loadleveler import QueryCategoryList, \
    QueryCategory, record_parser, value_saver
import json

with open('config_file_path', 'r') as f:
    config = json.load(f)
    
category_list = QueryCategoryList()
for an_item in config:
    category = QueryCategory(
        category_id=an_item['id'],
        display_name=an_item['display_name'],
        label=an_item['display_name'],
        record_parser_class=getattr(record_parser, an_item['record_parser_class']),
        record_parser_arguments=tuple(an_item['record_parser_arguments']),
        value_saver_class=getattr(value_saver, an_item['value_saver_class']),
        value_saver_arguments=tuple(an_item['value_saver_arguments'])
    )
    category_list.append(category)
```

Get `llq -l` command output.

```python
import subprocess

command = "/usr/bin/llq -l"
pipe = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
output = pipe.communicate()[0]
output_string = output.decode()
output_lines = output_string.split("\n")
```

Build `QueryModel` from `QueryCategoryList`

```python
from nwpc_hpc_model.loadleveler import QueryModel

model = QueryModel.build_from_category_list(output_lines, category_list)
```

`model` contains data of all categories in the config file.

## Test

Use `pytest` to run all tests.

## License

Copyright &copy; 2016-2017, Perilla Roc.

`nwpc-hpc-model` is licensed under [The MIT License](https://opensource.org/licenses/MIT).
