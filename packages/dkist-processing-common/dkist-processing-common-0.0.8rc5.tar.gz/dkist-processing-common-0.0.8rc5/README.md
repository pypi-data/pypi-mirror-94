# dkist-processing-common

This repository works in concert with `dkist-processing-core` and `dkist-processing-*instrument*` to form the DKIST calibration processing stack.

## Code overview

The code in this repository is organized into three main classes and a number of utility modules.
Tha main classes form a hierarchy as follows:
```text
   dkist-processing-instrument
        |               |
        |               |
*SupportBaseTask*  *ScienceBaseTask*
            |        |
            |        |
          *TaskBaseExt*
               |
               |
      dkist-processing-core
```

The `SupportBaseTask` class contains all the required functionality for interaction with other DKIST services, comprising of database interaction and messaging.

The `ScienceBaseTask` class handles provenance recording for any scientific manipulation of the data.

The `TaskBaseExt` class handles reading and writing of files and other objects.

## Usage

The classes in this repository should be used as the base of any DKIST processing pipeline tasks. Science tasks should subclass `ScienceTaskBase`, and all other tasks should subclass `SupportTaskBase`.

Each class is built on an abstract base class with the `run` method left for a developer to fill out with the required steps that the task should take.
This class is then used as the callable object for the workflow and scheduling engine.

## Example
```python
from dkist_processing_common.base import ScienceTaskL0ToL1

class RemoveArtifacts(ScienceTaskL0ToL1):
    def run(self):
        # task code here
        total = 2 + 5
```

## Deployment
dkist-processing-common is deployed to [PyPI](https://pypi.org/project/dkist-processing-common/)

## Development

```bash
git clone git@bitbucket.org:dkistdc/dkist-processing-common.git
cd dkist-processing-common
pre-commit install
pip install -e .[test]
pytest -v --cov dkist_processing_common
```
