#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name="praw-script-oauth",
	version="0.1.3",
	packages=find_packages(),
	install_requires=[
		"requests>=2.9"
	],
	description="Script OAuth utility for Reddit and PRAW",
	author="Tyler Haines",
	author_email = "theenigmablade@gmail.com",
	url="https://github.com/TheEnigmaBlade/praw-script-oauth",
	license="MIT",
	keywords=["reddit", "oauth", "praw"],
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Topic :: Internet",
		"Topic :: Software Development :: Libraries",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Utilities"
	],
)
