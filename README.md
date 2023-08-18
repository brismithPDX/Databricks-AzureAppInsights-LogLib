# Project Overview 

## purpose
To provide a method for publishing custom telemetry and code logs from their databricks instances to app insights in a single uniform command from any python notebook used.

## Author


# Getting Started
## Installation process:
1. configure a project level venv

    1.1 Create Virtual Python Environment
    ```
    $ python3 -m pip install --user virtualenv
    $ python2 -m venv env
    ```
    1.2 Enter the Python Virtual Environment
    ```
    $ source env/bin/activate
    ```
    1.3 Verify the You have activated the local directory virtual python environment
    ```
    $ which python3
    ```
    which should give you the result
    ```
    .../env/bin/python
    ```

2. install project dependencies
    ```
    python3 -m pip install opencensus-ext-azure
    ```

3. Environment is now ready to start development

## Software dependencies
- [python3](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
- [virtualenv](https://docs.python.org/3/library/venv.html)
- [json](https://docs.python.org/3/library/json.html)
- [opencensus-ext-azure](https://pypi.org/project/opencensus-ext-azure/)
- [logger](https://docs.python.org/3/library/logging.html)
- [Azure Databricks](https://azure.microsoft.com/en-us/services/databricks/)
- [Azure App Insights (appi)](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)


# Further Documentation
1. Raw Author Developer notes and test information available in the
    ```./docs/``` directory


