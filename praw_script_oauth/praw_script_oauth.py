_DEFAULT_USERAGENT = "script:Default praw-script-oauth useragent:v0.1.3 (by /u/TheEnigmaBlade)"
_DEFAULT_REDIRECT = "http://example.com/unused/redirect/uri"
_TOKEN_LENGTH = 3600000 # 1 hr

import logging
log = logging.getLogger("praw-script-oauth")

from time import time
from .config import read_config, write_config

def connect(oauth_key, oauth_secret, username, password, oauth_redirect=_DEFAULT_REDIRECT, oauth_scopes=set(), useragent=_DEFAULT_USERAGENT, script_key=None):
	"""
	Creates a PRAW instance using OAuth with the given authentication information.
	Because the retrieved token is stored on the file system (script_key is used to distinguish between files), this function is safe
	to call across multiple instances or runs. The token is renewed after one hour.
	
	Note: Only script-based oauth is supported.
	
	:param oauth_key:		Reddit oauth key
	:param oauth_secret: 	Reddit oauth secret
	:param username: 		Reddit username
	:param password: 		Reddit password
	:param oauth_redirect: 	Redirect used in registered Reddit app
	:param oauth_scopes: 	Set of scopes passed to PRAW
	:param useragent: 		Connection useragent (this should be changed, otherwise you'll be heavily rate limited)
	:param script_key: 		Key used to distinguish between local token files
	
	:return: A PRAW instance if a token could be retrieved, otherwise None.
	"""
	import praw
	
	oauth_token = get_oauth_token(oauth_key, oauth_secret, username, password, useragent=useragent, script_key=script_key)
	if oauth_token is None:
		log.debug("Can't create PRAW instance without token")
		return None
	
	r = praw.Reddit(user_agent=useragent, disable_update_check=True)
	r.set_oauth_app_info(oauth_key, oauth_secret, oauth_redirect)
	r.set_access_credentials(oauth_scopes, oauth_token)
	r.config.api_request_delay = 1
	return r

def get_oauth_token(oauth_key, oauth_secret, username, password, useragent=_DEFAULT_USERAGENT, script_key=None):
	"""
	Gets an OAuth token from Reddit or returns a valid locally stored token.
	Because the retrieved token is stored on the file system (script_key is used to distinguish between files), this function is safe
	to call across multiple instances or runs. The token is renewed after one hour.
	This function can be used without PRAW.
	
	Note: Only script-based oauth is supported.
	
	:param oauth_key:		Reddit oauth key
	:param oauth_secret: 	Reddit oauth secret
	:param username: 		Reddit username
	:param password: 		Reddit password
	:param useragent: 		Connection useragent (this should be changed, otherwise you'll be heavily rate limited)
	:param script_key: 		Key used to distinguish between local token files
	
	:return: An OAuth token if one could be retrieved, otherwise None.
	"""
	token = _get_local_token(script_key, username)
	if token is None:
		token_time = _time_ms()
		token = _request_oauth_token(oauth_key, oauth_secret, username, password, useragent=useragent)
		write_config(token, token_time, _get_config_file(script_key, username))
	return token

# Token access

def _get_local_token(script_key, username):
	token, token_time = read_config(_get_config_file(script_key, username))
	
	current_time = _time_ms()
	if (current_time - token_time) < _TOKEN_LENGTH:
		# Token is still likely valid
		return token
	
	return None

def _request_oauth_token(oauth_key, oauth_secret, username, password, useragent=_DEFAULT_USERAGENT):
	import requests
	from requests.auth import HTTPBasicAuth
	
	try:
		log.debug("Requesting OAuth token")
		# Make request
		client_auth = HTTPBasicAuth(oauth_key, oauth_secret)
		headers = {"User-Agent": useragent}
		data = {"grant_type": "password", "username": username, "password": password}
		response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, headers=headers, data=data)
		if not response.ok:
			# HTTP error code returned
			log.error("OAuth error code {}: {}".format(response.status_code, response.reason))
			return None
		response_content = response.json()
		if "error" in response_content and response_content["error"] != 200:
			# Reddit error in returned response data
			log.error("Response error: {}".format(response_content["error"]))
			return None
		
		# Check token type (doesn't really need to be done, but for sanity)
		token_type = response_content["token_type"]
		if token_type != "bearer":
			log.error("Received wrong type of token ({}), wtf reddit".format(token_type))
			return None
		
		return response_content["access_token"]
	
	except Exception as e:
		log.exception("Failed to retrieve token: {}".format(e))
		return None

# Utilities

def _get_config_file(script_key, username):
	key = "_{}".format(script_key) if script_key is not None and len(script_key) > 0 else ""
	user = "_{}".format(username) if username is not None and len(username) > 0 else ""
	return "oauth_store{}{}.txt".format(key, user)

def _time_ms():
	return int(time()*1000)
