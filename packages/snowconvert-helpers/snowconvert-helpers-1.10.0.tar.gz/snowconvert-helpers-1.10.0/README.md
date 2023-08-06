# SnowConvert Helpers

SnowConvert Helpers is a class of functions designed to facilitate the conversion of Teradata BTEQ script files
to Python files that Snowflake can interpret. Mobilize.Net SnowConvert for Teradata can take in any Teradata SQL or
scripts (BTEQ, FastLoad, MultiLoad, TPT, and TPump) and convert them to functionally equivalent Snowflake SQL,
JavaScript embedded in Snowflake SQL, and Python. Any output Python code from SnowConvert will call functions from this
helper class to complete the conversion and create a functionally equivalent output in Snowflake.

The [Snowflake Connector for Python](https://pypi.org/project/snowflake-connector-python/) will also be called in order 
to connect to your Snowflake account, and run the output python code created by SnowConvert.


For more information, visit the following webpages.

> More Information on Mobilize.Net SnowConvert for Teradata: https://www.mobilize.net/products/database-migrations/teradata-to-snowflake

> Mobilize.Net SnowConvert for Teradata Documentation: https://docs.mobilize.net/snowconvert/for-teradata/introduction

> User Guide for snowconvert-helpers: https://docs.mobilize.net/snowconvert/for-teradata/migration-helpers