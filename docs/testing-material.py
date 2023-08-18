
def main():
    logger = AppiLog("test", 20)

    #logger.warning("This is a library log WARNING", "DEMO4", details={"none":"none"})
    logger.exception("This is a library log EXCEPTION", "DEMO64", details={"none":"none"})
    #logger.info("This is a library log INFO", "DEMO44", details={"none":"none"})
    #logger.debug("This is a library log DEBUG", "DEMO44", details={"none":"none"})

    # clean up after log object in hopes databricks wont maintain duplicate state when a notebook is re-run w/out clearing
    del logger



main()



dbutils.secrets.get(scope="databricks-demo-scope", key="appi-conn-str")