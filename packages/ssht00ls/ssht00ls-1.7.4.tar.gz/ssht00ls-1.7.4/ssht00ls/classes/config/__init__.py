#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, pexpect, random

# inc imports.
from fil3s import Files, Formats
from r3sponse import r3sponse
import cl1, syst3m

# source.
ALIAS = "ssht00ls"
SOURCE_NAME = "ssht00ls"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=3)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}")

# universal variables.
OWNER = os.environ.get("USER")
GROUP = "root"
HOME_BASE = "/home/"
HOME = f"/home/{os.environ.get('USER')}/"
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["osx"]: 
	HOME_BASE = "/Users/"
	HOME = f"/Users/{os.environ.get('USER')}/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"

# check lib.
if not os.path.exists(f"{SOURCE_PATH}/lib"):
	print("Downloading ssht00ls library.")
	os.system(f"rm -fr /tmp/ssht00ls && git clone https://github.com/vandenberghinc/ssht00ls /tmp/ssht00ls && cp -r /tmp/ssht00ls/ssht00ls/lib {SOURCE_PATH}/lib")