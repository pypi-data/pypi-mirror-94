Change Log for Mercury Client API.
The format is based on [Keep a Changelog] (https://keepachangelog.com/en/1.0.0/)

##[1.0.0] - 2021-02-12
###Removed
- Support for Python 2
###Added
- Pydantic models for generating credit bureau requests [IN-317]
- Fetch CIBIL report functionality [IN-278]
- Fetch Highmark report functionality [IN-359]
- Incoming webhook verification method [IN-370]

##[0.5.0] - 2020-10-28
###Added
- New get_sms_result method to get result of SMS requests
###Fixed
- Constructing API URLs safely with urllib


##[0.4.0] - 2020-07-08
###Added
- Fetch Experian report functionality [IN-350]


##[0.3.0] - 2020-08-13
###Fixed
- tox support
- Send SMS functionality


##[0.2a1] - 2020-07-08
###Fixed
- Initialization issue in Mercury Client [IN-277](https://esthenostech.atlassian.net/browse/IN-277)


##[0.1a1] - 2020-07-07
###Fixed
- Installation issue in Python 2


## [0.1a] - 2020-07-06
###Added
- Mercury Client first cut
- Send Email functionality
