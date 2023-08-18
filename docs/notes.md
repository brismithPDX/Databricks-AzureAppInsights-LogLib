
# transferring data and context between notebooks in a job
sharing context between jobs in sequence for databricks is possible with the dbutils.jobs.taskValues commands, this allows us to retrieve context from any previous task in a databricks job run.

this ability is currently entirely unused.

in theory we could apply it to the start of any job with a single line and then retrieve later at for use in tracking and correlating log events

task 1 (dbutils.job.taskValues.set({name:$_jobName, other_detail:$_details})) -> task n-1 (dbutils.job.taskVaules.get(name) == $_jobName)

such a plan could be applied anywhere for any data with in a job run

# Getting Context in a notebook
```
dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson() 
```
CITATION: https://community.databricks.com/s/question/0D53f00001HKHkhCAH/is-it-possible-to-get-job-run-id-of-notebook-run-by-dbutilsnotbookrun


^ appears to imply that that dbutils.notebook.entry_point provides information about the current notebook context / runtime and may provide the ability to get contextual information about the task / notebook for logging

you can see a example of this export in the "example-notebookContext.json" file

it also appears that we can import the notebook run parameters from the following command
dbutils.notebook.entry_point.getCurrentBindings()

however i do not have a example one of these due to the lack of job based runs to experiment with

# implementing a log library

right now this is the officially supported documentation for azure + python
https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python

further proof of its work in databricks
https://medium.com/analytics-vidhya/azure-databricks-log-runtime-errors-to-application-insights-699586e23d15


# custom code based telemetry caveats
generally custom code telemetry can not be directly ingested by a log instance but must route though a appi instance. you can then however join these items from the log instance with the command.
```
union withsource=SourceApp 
app('[appi instance name]').[appi table name]
```

this allow you to mix and match logs from az infrastructure directly with code telemetry for single views and shared visualization.


CITATION: https://docs.microsoft.com/en-us/azure/azure-monitor/logs/unify-app-resource-data

# required libs on cluster imported from PyPi repo
opencensus-ext-azure
opencensus
opencensus-ext-logging

# brian's test Model for the dev cluster
---