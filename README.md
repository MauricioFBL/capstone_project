# capstone_project

## Description

The goal is to create an end-to-end solution; this problem reflects a real-world
scenario where a Data Engineer must configure the environment and resources,
integrate the data from external sources and clean the data and process it for
their further analysis. When the data is ready, transform it to reflect business
rules and deliver knowledge in the form of insights.


## Data Sources

The project consumes different datasets, which are dependent on manual 
processes or a software registries. The data is uploaded on AWS S3 and then 


## Development


### Requirements and Installation

directories and file structure:
```
    CAPSTONE PROJECT/
    |---infraestructure/
          |---aws
          |---kubernetes
    |---dags/
    |---notebooks/
    |---scripts/
    |---.gitignore
    |---README.md
    |---requirements.txt
```
This project runs on ubuntu20.04 and need the next tools to run aws_cli, helm, kubectl,
and terraform

To setup the infraestructure run de [set_infraestructure.sh](set_infraestructure.sh) file

`sh set_infraestructure.sh`

This will run the necesary command to set uo the infraestructure for the dags in AWS


It requires Python 3.8.10 or higher, check your Python version first.

The [requirements.txt](requirements.txt) should list and install all the required
Python libraries that the project depend on, and they can be installed using:

`pip install -r requirements.txt`