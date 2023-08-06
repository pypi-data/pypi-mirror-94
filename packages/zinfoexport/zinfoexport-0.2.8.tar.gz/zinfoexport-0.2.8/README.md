This package contains a client to make a data request from the z-info API.
--------------------------------------------------------------------------------------------------

To create a client you need a json file with the following parameters:

username: str\
    This is your z-info username\
password: str\
    This is your z-info password\
file_name: str\
    Name for your export file\
file_format: str\
    Can either be ".csv" or ".feather"\
input_file: str \
    Name for your input csv. It is mandatory to have a header row with these three values: tagnr, name, wbm\
startdate: str\
    Start date in YYYY-MM-DD format\
enddate: str\
    End date in YYYY-MM-DD format\
periode: str\
    time for which values will be aggregated. can be anything between 1-9 s/m/h (for example: 5m = 5 minutes)\
interval: str\
    To avoid making requests for too long intervals this spilts the dates up in intervals. Default is 10 which works fine.\
waterschapnummer: str\
    Waterschap specific number.\
spcid: str\
    Waterschap specific spcid.\

You then need to specify the file name to create a client.\
With this client you can use the method run to make a request based on your parameters.\
If you create a client without a parameters file, it will generate a template which you can then fill in and supply using the function set_parameters("name of your parameter file")