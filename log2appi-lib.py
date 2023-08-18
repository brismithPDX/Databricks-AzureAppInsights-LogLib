import logging
import json
import random
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.trace.propagation.text_format import TextFormatPropagator
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.span_context import SpanContext

# Define databricks integration components
from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
dbutils = DBUtils(spark)

config_integration.trace_integrations(['logging'])

# Define our logger Class
class AppiLog:
    # class values

    ## get the databricks execution context
    __class_context = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
    ## build the default custom properties
    __properties = json.dumps({'rootRunId': __class_context["rootRunId"], 
        'currentRunId': __class_context["currentRunId"],
        'notebookId': __class_context["tags"]["notebookId"],
        'notebookPath': __class_context["extraContext"]["notebook_path"]})

    # constructor
    def __init__(self, name, level) -> None:
        self._logger = logging.getLogger(name)  # initialize a logger agent
        self._name = name

        # configure the log level
        self._logger.setLevel(level)

        # enable appi log publishing
        handler = AzureLogHandler(component_name= self._name ,connection_string = '[APP Insights Key - REPLACE with ENV VAR]')
        handler.setFormatter(logging.Formatter('%(message)s'))
        self._logger.addHandler(handler)

        # enable tracer spans and context, prioritizing pre-existing
        self._span_context = None

        carrier = {
            "opencensus-trace-traceid" : self.__genTraceID(),
            "opencensus-trace-spanid"  : self.__genSpanID()
        }
        self._span_context = TextFormatPropagator().from_carrier(carrier)

        # enable tracing for the log context
        traceExporter = AzureExporter(connection_string = '[APP Insights Key - REPLACE with ENV VAR]')
        self._tracer = Tracer(
            span_context = self._span_context,
            exporter = traceExporter,
            sampler = ProbabilitySampler(1.0)
        )

        # preform initialization logging for tracing
        init_message = self._name + " : Notebook Logging init "
        self._logger.info(init_message, extra=self.__buildProperties("Log Context Message", {}))

    # destructor: clean up, publish all logs, and clear out the log
    def __del__(self) -> None:
        while self._logger.hasHandlers():
            self._logger.handlers[0].flush()
            self._logger.removeHandler(self._logger.handlers[0])

    # public logging functions
    def warning(self, message, type_category="default", details={}) -> None:
        # build and merge all custom log properties
        props = self.__buildProperties(type_category, details)
        # ship the log to appi
        self._logger.warning(message, extra=props)

    def exception(self, message, type_category="default", details={}) -> None:
        print("normal exception")
        props = self.__buildProperties(type_category, details)
        self._logger.exception(message, extra=props)

    def info(self, message, type_category="default", details={}) -> None:
        props = self.__buildProperties(type_category, details)
        self._logger.info(message, extra=props)

    def debug(self, message, type_category="default", details={}) -> None:
        props = self.__buildProperties(type_category, details)
        self._logger.debug(message, extra=props)

    def export_traceContext(self) -> dict:
        carrier = {}
        TextFormatPropagator().to_carrier(self._span_context,carrier)
        return carrier

    def write_traceContext2DataBricks(self) -> None:
        carrier = {}
        TextFormatPropagator().to_carrier(self._span_context,carrier)

        dbutils.jobs.taskValues.set(key   = "traceID", \
                                    value = carrier.get("opencensus-trace-traceid"))
        dbutils.jobs.taskValues.set(key   = "traceOptions", \
                                    value = carrier.get("opencensus-trace-traceoptions"))


    # private support functions
    def __buildProperties(self, category, extra_props = {}) -> dict:
        # create custom properties object
        final_props={"category": category,
        "code_context": json.dumps(extra_props),
        "db_context": self.__properties,
        "LogInstanceName": self._name}

        return {'custom_dimensions': final_props}

    def __isInJob(self) -> bool:
        jobName = self.__class_context["tags"]["jobName"]
        if(jobName == 'Untitled'):
            return False
        else:
            return True

    def __genTraceID(self) -> str:
        rd = random.Random()
        rd.seed(self.__class_context["currentRunId"]["id"])
        return '{:032x}'.format(rd.getrandbits(128))
    
    def __genSpanID(self) -> str:

        if (self.__class_context["rootRunId"]["id"] == self.__class_context["currentRunId"]["id"]):
            return None
        else:
            rd = random.Random()
            rd.seed(self.__class_context["rootRunId"]["id"])
            return '{:016x}'.format(rd.getrandbits(128))