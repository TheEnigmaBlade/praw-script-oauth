# PRAW script OAuth

Utility for using script OAuth with Reddit and PRAW. OAuth tokens are cached and can be used across multiple instances and executions.

While utility for creating PRAW instances including OAuth information is included, **PRAW is not required** to use all of this library's functions. If you use PRAW functions, you must install PRAW >= 3.0.

* Use `connect(oauth_key, oauth_secret, username, password)` to retrieve an OAuth token *and create a PRAW instance*. The optional, but recommended, parameters are:
    * `oauth_redirect` (default `"http://example.com/unused/redirect/uri"`)
    * `oauth_scopes` (set of scope strings, default `set()`)
    * `useragent` (Reddit requires your own)
    * `script_key` (used to distinguish local token files, default `None`)
* Use `get_oauth_token(oauth_key, oauth_secret, username, password)` to retrieve an OAuth token. *PRAW is not required.* The optional parameters are:
    * `useragent` (Reddit requires your own)
    * `script_key` (used to distinguish local token files, default `None`)

## Install

    pip install praw-script-oauth

Or [from the PyPI site](https://pypi.python.org/pypi/praw-script-oauth).
