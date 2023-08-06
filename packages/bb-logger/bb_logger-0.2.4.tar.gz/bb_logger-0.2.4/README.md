# BB LOGGER
## Description
1. Remove all logger handlers and reformat log record ( can be extended )
2. Set noti status, controlable by arguments
3. Override lambda raise error to critical and notice if noti status = True, optional


## How
> 1. call setup_logging() one time at begin of program
> 2. using decorator setup_logging_dec() with each lambda

### Params
> **default_level** (int, optional): min log level. Defaults to logging.WARNING.

> **extend_format** (str, optional): custom extend format. Defaults to None.

> **lambda_exec_error_log** (bool, optional): log with critical level for lambda raise exception. Defaults to True. only with decorator **setup_logging_dec()**

> **default_noti_level** (int, optional): all log from this level will be noticed if no arguments are provided. Defaults to logging.ERROR

> **force_noti_level** (int, optional): force all log with this level to be noticed. Defaults to logging.ERROR.

#### Notes

> (*) extend_format logic

logging format details can be  [here](https://docs.python.org/3/library/logging.html#logrecord-attributes)

* BASE_FORMAT = '[%(levelname)s]'
* DEFAULT_FORMAT = BASE_FORMAT + ' %(message)s'
* if extend_format is specified, FORMAT will be : BASE_FORMAT + '\\t'+ extend_format
* else DEFAULT_FORMAT wil be used  
##  EXAMPLES
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





 ### 2. Set noti status

 ADD NOTI STATUS TO LOG BASE ON CONDITIONS
 > (*) **force_noti_level** : default is logging.ERROR

EXAMPLE

```python
import logging
from bb_logger import setup_logging
logging.error('before setup')
# setup log with default 
setup_logging()
logging.error('after setup, noti status was added')

# specify if this log will be noticed or not
logging.warning('warning with noti True', {'noti': True})
logging.warning('warning with noti False', {'noti': False})

# set force noti level
setup_logging(default_level=logging.INFO, force_noti_level=logging.INFO)
logging.info('info with noti True', {'noti': True})
logging.info('info with noti False stil have NOTI status', {'noti': False})


```
> output
```sh
[ERROR]	2021-02-06T08:01:56.558Z	c4c3fad9-eacf-41f3-bba1-15b119bfd980	before setup
[ERROR] [NOTI] after setup, noti status was added
[WARNING] [NOTI] warning with noti True
[WARNING] [NOT_NOTI] warning with noti False
[INFO] [NOTI] info with noti True
[INFO] [NOTI] info with noti False stil have NOTI status

```


###  Override lambda raise error to critical

EXAMPLE

```python
from bb_logger import setup_logging,setup_logging_dec

@setup_logging_dec(default_level=logging.INFO,lambda_exec_error_log=True, force_noti_level=logging.ERROR)
def lambda_handler(event, context):
    a = 1 / 0

```
> output
```shell
[CRITICAL] [NOTI] division by zero
Traceback (most recent call last):
  File "/var/task/bb_logger.py", line 98, in wrapper
    func(*args, **kwargs)
  File "/var/task/lambda_function.py", line 12, in lambda_handler
    a = 1/ 0
```
> exception raise by lambda will be set at Critical level and noticed



## NOTE

CloudWatch now accept following pattern:

* [LEVEL] [NOTI]

Example:

* "[ERROR] [NOTI] error log" will be matched

* "some thing before [ERROR] [NOTI] error log" will be matched