[![PyPI version](https://badge.fury.io/py/fameio.svg)](https://badge.fury.io/py/fameio)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4501190.svg)](https://doi.org/10.5281/zenodo.4501190)
[![PyPI license](https://img.shields.io/pypi/l/fameio.svg)](https://badge.fury.io/py/fameio)
[![pipeline status](https://gitlab.com/fame-framework/fame-io/badges/main/pipeline.svg)](https://gitlab.com/fame-framework/fame-io/commits/main)


# FAME-Io 
Python scripts for FAME models, generation of protobuf input files and conversion of protobuf output files.
Please visit the [FAME-Wiki](https://gitlab.com/fame-framework/fame-wiki/-/wikis/home) to get an explanation of FAME and its components.
The package is also formerly known as [FAME-Py](https://doi.org/10.5281/zenodo.4314338).

# Installation

    pip install fameio

# Usage
FAME-Io currently offers two main scripts "makeFameRunConfig" and "convertFameResults".
Both are automatically installed with the package.
The first one creates a protobuf file for FAME applications using YAML definition files and .csv files.
The latter one reads output files from FAME applications in protobuf format and converts them to .csv files.

## Make a FAME run configuration
Digests configuration files in YAML format, combines them with .csv files and creates a single input file for FAME applications in protobuf format.
Call structure:

    makeFameRunConfig -f <path/to/scenario.yaml>
   
You may also specify any of the following arguments:

|Command  |Action|
|-----------|-----|
|`-l` or `--log` |Sets the logging level. Default is `warn`. Options are `debug`, `info`, `warning`, `warn`, `error`, `critical`.|
|`-lf` or `--logfile` |Sets the logging file. Default is `None`. If `None` is provided, all logs get only printed to the console.|
|`-o` or `--output` |Sets the path of the compiled protobuf output file. Default is `config.pb`.|

This could look as follows:

    makeFameRunConfig -f <path/to/scenario.yaml> -l debug -lf <path/to/scenario.log> -o <path/to/config.pb>
    
    
You may also call the configuration builder from any Python script with

```python
from fameio.scripts.make_config import run as make_config

make_config("path/to/scenario.yaml")
```

Similar to the console call you may also specify custom run config arguments and add it in a dictionary to the function call.

```python
import logging as log

from fameio.scripts.make_config import run as make_config

run_config = {"log_level": log.DEBUG,
              "output_file": "output.pb",
              "log_file": "scenario.log",
              }

make_config("path/to/scenario.yaml", run_config)
```


### Scenario YAML
The "scenario.yaml" file contains all configuration options for a FAME-based simulation. 
It consists of the sections `Schema`, `GeneralProperties`, `Agents` and `Contracts`, all of them described below.

#### Schema
The Schema is used to validate the inputs of the "scenario.yaml". 
Since the Schema should be valid across multiple scenarios, it is recommended to defined it in a separate file and include the file here.  

Currently, the schema specifies:
* which type of Agents can be created
* what type of input fields an Agent uses
* what type of Products an Agent can send in Contracts.

The Schema consists of the sections `Header` and `AgentTypes`.

##### Header
The header specifies information about a FAME-based application for which input files are to be created. 
The idea here is to tie a schema.yaml to a specific version the application, ensuring a match between the inputs required by the application and those provided by the configs to be created. 

```yaml
Header:
  Project: MyProjectName
  RepoUrl: https://mygithosting.com/myProject
  CommitHash: abc123
```

* `Project` name of your project / FAME-based application
* `RepoUrl` URL of your project
* `CommitHash` hash of the commit / version of your project
 
##### AgentTypes
Here, each type of agent that can be created in your FAME-based application is listed, its input fields and its available Products for Contracts. 

```yaml
AgentTypes:
  <MyAgentWithAttributes>:
    Attributes:
      <<MyAttributeName>>:
        FieldType: enum
        Mandatory: true
        Values: [ 'AllowedValue1', 'AllowedValue2' ]
    Products: [ 'Product1' ]

  <MyAgentWithoutAttributes>:
    Products: [ 'ProductA', 'ProductB' ]
```

* `<MyAgentName>` Java's simple class name of the Agent type; be sure to remove brackets <>
* `<<MyAttributeName>>` Name of the input field as specified in the Java enum annotated with "@Input"; be sure to remove brackets <<>>
* `FieldType` data type of the input field; currently the types "INTEGER, DOUBLE, ENUM, TIME_SERIES" are supported
* `Mandatory` if true: the field is required for this agent
* `Values` optional parameter: if present defines a list of allowed values for this input field
* `Products` list of Products that this Agent can send in Contracts; derived from Java enum  annotated with "@Product"    


#### GeneralProperties
Specifies FAME-specific properties of the simulation. Structure:

```yaml
GeneralProperties:
  RunId: 1
  Simulation:
    StartTime: 2011-12-31_23:58:00
    StopTime: 2012-12-30_23:58:00
    RandomSeed: 1
  Output:
    Interval: 100
    Process: 0
```

Parameters:
* `RunId` an ID that can be given to the simulation; use at your discretion
* `StartTime` time stamp in format YYYY-MM-DD_hh:mm:ss; first moment of the simulation.
* `StopTime` time stamp in format YYYY-MM-DD_hh:mm:ss; last moment of the simulation - i.e. simulation terminates after passing that time stamp
* `RandomSeed` seed to initialise random number generation; each value leads to a unique series of random numbers.
* `Interval` number of simulation ticks in between write-to-disk events; may be used for performance optimisations; 
* `Process` id of process that performs write-to-disk operations; leave at 0 to be compatible with single-processes;

#### Agents
Specifies all Agents to be created in the simulation in a list. Each Agent has its own entry. 
Structure:
```yaml
Agents:
  - Type: MyAgentWithInputs
    Id: 1
    Attributes:
      MyEnumField: SAME_SHARES
      MyIntegerField: 2
      MyDoubleField: 4.2
      MyTimeSeriesField: "./path/to/time_series.csv"

  - Type: MyAgentWithoutInputs
    Id: 2
```


Agent Parameters:
* `Type` Mandatory; Java's simple class name of the agent to be created 
* `Id` Mandatory; simulation-unique id of this agent; if two agents have the same ID, the configuration process will stop. 
* `Attributes` Optional; if the agent has any Input fields, specify them here in the format "FieldName: value"; please see input value table below

|FieldType  |value|
|-----------|-----|
|INTEGER |integer numeric value|
|DOUBLE|numeric value (integer or floating point)|
|ENUM|String(name of associated enum value)|
|TIME_SERIES|String representing path to .csv file|

The specified `Attributes` for each agent must match the specified `Attributes` options in the linked Schema YAML (see above).

#### Contracts
Specifies all Contracts, i.e. repetitive bilateral transactions in between agents. Contracts are given as a list.
We recommend to move Contracts to a separate file or files in a separate folder and to use the `!include` command to use them here.

```yaml
Contracts:
  - SenderId: 1
    ReceiverId: 2 
    ProductName: ProductOfAgent_1
    FirstDeliveryTime: -25
    DeliveryIntervalInSteps: 3600

  - SenderId: 2
    ReceiverId: 1
    ProductName: ProductOfAgent_2
    FirstDeliveryTime: -22
    DeliveryIntervalInSteps: 3600
```

Contract Parameters:
* `SenderId` unique Id of agent sending the product
* `ReceiverId` unique Id of agent receiving the product
* `ProductName` name of the product to be sent
* `FirstDeliveryTime` first time of delivery in format "seconds after the January 1st 2000, 00:00:00" 
* `DeliveryIntervalInSteps` delay time in between deliveries in seconds

### CSV files
TIME_SERIES inputs are not directly fed into the Scenario YAML file.
Instead, TIME_SERIES reference a .csv file that can be stored some place else.
These .csv files follow a specific structure:
* They must contain exactly two columns.
* The first column must be a time stamp in form YYYY-MM-DD_hh:mm:ss
* The second column must be a numerical value (either integer or floating point)
* The separator of the two columns is a semicolon

Exemplary content of a valid .csv file:

    2012-01-01_00:00:00;400
    2013-01-01_00:00:00;720.5
    2014-01-01_00:00:00;650
    2015-01-01_00:00:00;99.27772
    2016-01-01_00:00:00;42
    2017-01-01_00:00:00;0.1

### Split and join multiple YAML files
The user may include other YAML files into a YAML file to divide the content across files as convenient.
We explicitly recommend to use this feature for the `Schema` and `Contracts` sections.
Otherwise, the scenario.yaml may become crowded.

#### Command: !Include
To hint YAML to load the content of another file use `!include "path/relative/to/including/yaml/file.yml"`.
You can concatenate !include commands and can use !include in the included file as well.
The path to the included file is always relative to the file using the !include command.
So with the following file structure

###### file-structure
```
a.yaml
folder/b.yaml
folder/c.yaml
folder/deeper_folder/d.yaml
```
the following !include commands work

###### in a.yaml
```
ToBe: !include "folder/b.yaml"
OrNot: !include "folder/deeper_folder/d.yaml"
```

###### in b.yaml
```
ThatIs: !include "c.yaml"
TheQuestion: !include "deeper_folder/d.yaml"
```

Provided that 
###### in c.yaml
```
Or: maybe 
```
###### d.yaml
```
not: "?" 
```
the resulting file would look like this:

###### joined file a.yaml
```
ToBe:
  ThatIs: 
    Or: maybe
  TheQuestion: 
    not: "?"
OrNot: 
  not: "?"
```

You may also specify absolute file paths if preferred by starting with a "/".
 
When specifying only a file path, the complete content of the file is assigned to the given key.
You always need a key to assign the !include command to. 
However, you cannot combine the value returned from !include with other values in the same key.
Thus, the following combinations do not work:
###### caveats.yml
```
!include "file.yaml" # no key assigned

Key:
  Some: OtherItem
  !include "file.yaml" # cannot join with other named items

List:
  - an: entry
  !include "file.yaml" # cannot directly join with list items, even if !include returns a list 
```

#### Integrate specific nodes of YAML files
Instead of including *all* of the content in the included file, you may also pick a specific node within that file.
For this use `!include [<relative/path/to/file.yaml>, Path:To:Field:In:Yaml]`. 
Here, `:` is used in the node-specifying string to select a sequence of nodes to follow - with custom depth.
Consider the following two files:

###### file_to_be_included.yaml
```yaml
Set1:
  Subset1:
    Key: Value
Set2:
  OtherKey: OtherValue
```

###### including_file.yaml
```yaml
- Type: MyAgentWithInputs
  Id: 1
  Attributes: !include_node [file_to_be_included.yaml, Set1:Subset1]
```

Compiling "including_file.yaml" results in

###### resulting_file.yaml
```yaml
- Type: MyAgentWithInputs
  Id: 1
  Attributes: 
    Key: Value
```

#### Load multiple files
Using wildcards in the given path (e.g. "path/to/many/*.yaml") will lead to loading multiple files and assigning their content to the same key.
You can make use of this feature with or without specifying a node selector.
However, the elements to be joined across multiple files must be lists. 
These lists are then concatenated into a single list and then assigned to the key in the file calling !include.
This feature is especially useful for Contracts: You can split the Contracts list into many separate files and place them in a separate folder.
Them use !include to re-integrate them into your configuration. An example:
###### my_contract1.yaml
```
Contracts:
 - ContractA
 - ContractB
```
###### my_contract2.yaml
```
Contracts:
 - ContractC
 - ContractD
 - ContractE
```
###### including_file.yaml
```
Contracts: [!include "my_contract*.yaml", "Contracts"] 
```

results in
###### result.yaml
```
Contracts:
 - ContractA
 - ContractB
 - ContractC
 - ContractD
 - ContractE
```

#### Ignoring files
Files that have their name start with "IGNORE_" are not included with the !include command.
You will see a debug output to notify you that the file was ignored.
Use this to temporarily take files out ouf your configuration without deleting or moving them.

## Read FAME results
Takes an output file in protobuf format of FAME-based applications and converts it into files in .csv format.
An individual file for each type of Agent is created in a folder named after the protobuf input file.
Call structure:

    convertFameResults -f <./path/to/protobuf_file.pb> 

You may also specify any of the following arguments:

|Command  |Action|
|-----------|-----|
|`-l` or `--log` |Sets the logging level. Default is `warn`. Options are `debug`, `info`, `warning`, `warn`, `error`, `critical`.|
|`-lf` or `--logfile` |Sets the logging file. Default is `None`. If `None` is provided, all logs get only printed to the console.|
|`-a` or `--agents` |If specified, only a subset of agents is extracted from the protobuf file. Default is `None`.|

This could look as follows:

    convertFameResults -f <./path/to/protobuf_file.pb> -l debug -lf <path/to/output.log> -a AgentType1 AgentType2

You may also call the conversion script from any Python script with

```python
from fameio.scripts.convert_results import run as convert_results

convert_results("./path/to/protobuf_file.pb")
```

Similar to the console call you may also specify custom run config arguments and add it in a dictionary to the function call.

```python
import logging as log

from fameio.scripts.convert_results import run as convert_results

run_config = {"log_level": log.DEBUG,
              "log_file": "scenario.log",
              "agents_to_extract": ['AgentType1', 'AgentType2'],
              }

convert_results("./path/to/protobuf_file.pb", run_config)
```


# Update protobuf definitions
In case updated versions of protobuf definitions from FAME-Protobuffer shall be used, simply update the files in folder protobuf_definitions: 
* Contract_pb2.py
* InputFile_pb2.py
* Services_pb2.py

Make sure to fix relative import of `Contract_pb2` in `InputFile_pb2.py` by adding `from fameio.protobuf_definitions` 
in front of the auto-generated import statements. This is a known but not closed issue from
Google protobuf compiler.

# Contribute
Please read the Contributors License Agreement (cla.txt), sign it and send it to fame@dlr.de before contributing. 
