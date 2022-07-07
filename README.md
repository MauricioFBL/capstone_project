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
    LH4_AMPPS_DASH/
    |---infraestructure/
          |---aws
          |---kubernetes
    |---dags/
    |---.gitignore
    |---README.md
    |---requirements.txt
```

It requires Python 3.8.10 or higher, check your Python version first.

The [requirements.txt](requirements.txt) should list and install all the required Python 
libraries that the project depend on, and they can be installed using:

`pip install -r requirements.txt`

To create the project you have to execute [create_sos_soe.py](create_sos_soe.py) file:



This will run the ETL process, and write the output to the specified output
location.
