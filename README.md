# PRAW script OAuth

Utility for using script OAuth with Reddit and PRAW. OAuth tokens are cached and can be used across multiple instances and executions.

While utility for creating PRAW instances including OAuth information is included, **PRAW is not required** to use all of this library's functions. If you use PRAW functions, you must install PRAW >= 3.0.

* Use `connect(...)` to retrieve an OAuth token and create a PRAW instance.
* Use `get_oauth_token(...)` to retrieve an OAuth token.

## Install

    pip install praw-script-oauth

Or [from the PyPI site](https://pypi.python.org/pypi/praw-script-oauth).
