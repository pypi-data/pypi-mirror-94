# BB LOGGER
## Description
1. Remove all logger handlers and reformat log record ( can be extended )

2. Provide some other logging method than default (info, error..)

## How
> call setup_logging() one time at begin of program
### 1. Remove all logger handlers and reformat log record 

> sample code
```python 
import logging
from bb_logger import setup_logging

logging.error('before setup, using old handler format')
# setup log with default 
setup_logging()
logging.error('after setup, using new default format')
# setup logger with extend format
setup_logging(extend_format="%(asctime)s - %(message)s")
logging.error('after setup with custom format, using extended format')
```
> output 
```sh
ERROR:root:before setup, using old handler format
[ERROR] after setup, using new default format
[ERROR]	2021-01-10 18:18:46,202 - after setup with custom format, using extended format
```

logging format details can be  [here](https://docs.python.org/3/library/logging.html#logrecord-attributes)

> (*) extend_format logic

* BASE_FORMAT = '[%(levelname)s]'
* DEFAULT_FORMAT = BASE_FORMAT + ' %(message)s'
* if extend_format is specified, FORMAT will be : BASE_FORMAT + '\\t'+ extend_format
* else DEFAULT_FORMAT wil be used  


 ### 2. Provide some other logging method than default(info, error..)

 NOW SUPPORTED CUSTOM LEVEL (will be filtered and notify to slack, telegram, etc):
 * NOTI 


EXAMPLE
> must be used with logger, default logging will raise Error

```python
import logging
from bb_logger import setup_logging
setup_logging()
logger = logging.getLogger()
logger.noti('noti level')

```
> output
```shell
[NOTI] noti level
```



## NOTE

CloudWatch now accept following pattern:

* [ERROR]
* [CRITICAL]
* [NOTI]

Example:

* "[ERROR] error log" will be matched

* "some thing before [ERROR] error log" will be matched