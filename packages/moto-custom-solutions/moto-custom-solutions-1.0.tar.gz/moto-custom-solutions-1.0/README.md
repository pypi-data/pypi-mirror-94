### MOTO CUSTOM SOLUTIONS
### V 1.0

-----------------------
--> INSTALLING LIBRARY
-----------------------

- (Coming Soon) pip install motolibrary 

---------------------
--> IMPORTING MODULE
---------------------

- import motolibrary.motocustomsolutionspkg
- from motolibrary.motocustomsolutionspkg.(FileName.py) import (Function or \*)

----------------
||    DOCS    ||
----------------

The following is documentation for each of the library's functions:

---------------------
---> 1. dir\_clean.py
---------------------

Functionality: Removes all excel and csv files from a given directory.

Parameters:
  folder\_path : string
    (Optional) Path to directory containing files to delete.
    If not specified, deletes from current inventory.

Returns: None

Side Effects:
  Deletes all .xlsx and .csv files from specified local directory

Test Files for Function: test\_dir\_clean.py

------------------
---> 2. errors.py
------------------

Functionality: Defines errors for library use.

Classes:
  CustomError(Exception)
  DataError(CustomError)
  FTPConnectionError(CustomError)
  FTPUploadError(CustomError)
  FTPEncodingError(CustomError)
  RedashAPIError(CustomError)

-----------------------
---> 3. ftp\_cleanse.py
-----------------------

Functionality: Fills a dataframe with dummy values in each of the columns of which the original dataframe had data in.

Parameters:
  ftp\_df : pandas.DataFrame
    DataFrame with data that will be closed.
    All columns filled in this DataFrame will be replaced with dummy values in the returned DataFrame.

Returns:
  dummy\_df : pandas.DataFrame
    Dummy DataFrame containing only one row, of dummy values filled in the same columns as those that were filled in the original DF.

Ex. A DataFrame is passed with 3 columns, #1 and #3 are filled and #2 is not. The return would be a DF with the same
columns as the original, containing only one row with columns #1 and #3 would be filled with garbage text and #2 empty.

Test Files for Function: test\_ftp\_cleanse.py

--------------------
---> 4. ftp\_down.py
--------------------

Functionality: Downloads a file from an FTP server to a specified directory on the local machine.

Parameters:
  hostname : String
    FTP Host Name
  username : String
    FTP Login Username
  password : String
    FTP Login Password
  filename\_filter : String
    Name of file to download from FTP
  download\_directory : String 
    Directory to download file to. Default is CWD.

Returns: None

Test Files for Function: test\_ftp\_down.py

------------------
---> 5. ftp\_up.py
------------------

Functionality: Uploads a file from the local machine to a specified FTP server with an optional specified upload name.

Parameters:
  hostname : String
    FTP Host Name
  username : String
    FTP Login Username
  file\_name : String
    FTP Login Password
  upload\_name : String
    !! MUST INCLUDE EXTENSION !!
    (Optional) Specifies name of FTP Upload
      ie. Can be uploaded with a different name than local file.


Notes: File name must include its extension. So must the optional upload name.

Returns:
  True if supplement has been uploaded to FTP
  False if supplement did not upload to FTP

Test Files for Function: test\_ftp\_up.py

---------------------------
---> 6. redash\_download.py
---------------------------

Functionality: Downloads data from a Redash query (with optional additional params) to the local machine as a .csv file.

Parameters:
  query\_id : String
    ID of Redash Query
  api\_key : String
    User API Key
  region : String
    Country for Redash (ie. CA or US)
  file\_name : String
    File will be downloaded and saved locally as a .csv with this name
  params : Dictionary
    (Optional) Dictionary of query params -- Default = {} (empty)

Notes: The file name parameter should not include an extension. All query data will be processed & downloaded as a .csv file.
For example, if one calls the function with "redash\_data" as the file\_name argument, the query will be saved under "redash\_data.csv".

The region argument must be one of the following strings: ca, us, usa (capitalization does not matter... CA, US, USA will work).

Returns: None

Potential Errors Raised:
- ValueError (indicates invalid region code)
- RedashAPIError (connection issue with Redash API or invalid query info)

Test Files for Function: test\_redash\_download.py

-----------------------
---> 7. slack\_funcs.py
-----------------------

Functionality: Send messages or files to a list of Slack of channels.

Parameters:
- slack\_send\_file:
    slackbot_token : String
      Token for SlackBot Usage
    channels : List
      Contains list of channels to send to
    files : List
      Contains list of files to send
    titles : List
      Contains list of titles of files; titles should correspond to the same
      order of items in the files list.

- slack\_send\_message:
    slackbot_token : String
      Token for SlackBot Usage
    channels : List
      Contains list of channels to send messages to via slack
    messages : List
      Contains list of messages to send

Notes: For slack\_send\_file, the Titles list argument must perfectly match up to the Files list argument.

Returns: None

Test Files for Functions: test\_slack\_funcs.py    !! These are not automated tests - Manual checking of slack channels is needed !!

-----------------------
---> 8. supp\_create.py
-----------------------

Functionality: Creates a standard supplement file from a DataFrame whose columns are mapped to the supplement at the user's discretion. 

Parameters:
  df : pandas.DataFrame
    Pandas DataFrame containing data needed to be mapped into a supplement
  dealership\_col : String
    Name of column from df to map to Dealership UID column of Supplement
  vin\_col : String
    Name of column from df to map to VIN columnt of Supplement
  stock\_col : String
    Name of column from df to map to Stock column of Supplement
  trim\_col : String
    Name of column from df to map to Trim column of Supplement
  jato\_col : String
    (Optional) Name of column from df to map to JATO column of Supplement
  chrmstyle\_col : String
    (Optional) Name of column from df to map to Chrmstyle_ID column of Supplement
  discount\_col : String
    (Optional) Name of column from df to map to Discounts column of Supplement
  misc1\_col : String
    (Optional) Name of column from df to map to Misc 1 column of Supplement
  misc2\_col : String
    (Optional) Name of column from df to map to Misc 2 column of Supplement

Returns:
  supp\_df : pandas.DataFrame
    Supplement-style DataFrame with newly mapped data.

Ex. If one passes "my-dealerships" as the dealership\_col parameter, the supplement's Dealership UID column will contain data from the original file's "my-dealerships" column.

Test Files for Functions: test\_supp\_create.py 
