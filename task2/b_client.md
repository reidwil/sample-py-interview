# Loading CSVs to Snowflake
Author: Reid Williams

------
### 0. Setting env vars
As discussed in the actual python file, storing personal information in clear text is never a good idea. This opens yourself and your team up to external users getting access to your information. Instead, storing your secrets and passwords as environment variables is a good alternative (another even better idea is your service provider’s key vault but we will disregard for now).

The environment variables we need are:
 - `SNOWFLAKE_USER`
 - `SNOWFLAKE_PASSWORD`
 - `SNOWFLAKE_ACCOUNT`

We set environment variables by opening up our `.bash_profile` and storing the values there using this syntax. (Hint: you can open your bash_profile from terminal with this command: `open ~/.bash_profile`)

```
# ~/.bash_profile
export SNOWFLAKE_USER='your_username'
export SNOWFLAKE_PASSWORD='your_password'
export SNOWFLAKE_ACCOUNT='SNOWFLAKE_ACCOUNT'
```
Once the file is saved, we should be able to verify these exists by echoing their value:

`$ echo $SNOWFLAKE_USER` -> your_username


## 1. Installing python packages

I've attached a requirements.txt file for you to download the necessary files from.

To do that run this command in your terminal:
`$ pip install -r requirements.txt`

## 2. Running the script

To run the script you should command into the directory where the script is and run this command:

`python3.8 client_script.py path/to/csv/files database.schema.name`

Where the arguments after the calling of the `.py` files are the 1. the path to the csvs and 2. the name of the table to copy them into.


