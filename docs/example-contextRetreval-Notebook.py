
# Retrieve and Display the runtime context for this() runtime env from the cluster
context = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson() 
print("Execution Context: \n")
print(context)

print("\n\n")

# get and Display binding run parameters for this() runtime env 
run_parameters = dbutils.notebook.entry_point.getCurrentBindings()
print("Runtime Parameters: \n")
print(run_parameters)
