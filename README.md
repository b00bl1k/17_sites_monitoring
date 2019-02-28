# Sites Monitoring Utility

# Installation

Requires Python 3. To install, run `pip install -r requirements.txt`.

# Example of usage

Prepare file with urls for checking:

```
https://habr.com
http://eruina.com
http://random-url.com
https://github.com
https://мвд.рф
```

Run script:

```bash
$ python check_sites_health.py urls.txt
Domain           Is available   Is prepaid   Expiration date
habr.com         Yes            Yes          2023-03-11 17:04:56
eruina.com       No             No           2018-12-11 08:21:15
random-url.com   No             No           None
github.com       Yes            Yes          2020-10-09 18:20:50
мвд.рф           Yes            Yes          2019-11-24 15:04:00
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
