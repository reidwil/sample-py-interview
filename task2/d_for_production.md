### For production
- Add a logging class that we can use to debug output and errors a bit better
- Containerize this inside of a docker image
- Use CI to handle deployment and new integrations
- Depending on the machine, parallelize the csv reading/copying into snowflake
- Separate out the code into necessary sub dirs
- Write a few unit tests to assert the methods work appropriately
