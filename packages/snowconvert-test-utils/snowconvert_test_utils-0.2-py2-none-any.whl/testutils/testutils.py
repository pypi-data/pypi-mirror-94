import os
import subprocess
import sys
import time
from sys import stderr
from dotenv import load_dotenv
from sys import platform
import io

PYTHON = "python"

if platform == "darwin":
    # OS X
    PYTHON = "python3"

# current path will return the workspace
currentpath = os.getcwd()
currentdir = os.path.dirname(currentpath)

class ProcessResults:
    returncode = -1
    stdout = ""
    stderr = ""

def run(script):
    REPO_ROOT = os.environ['GITPOD_REPO_ROOT']
    COVERAGE_DIR = os.path.join(REPO_ROOT,".snowqm","coverage_data")
    # make sure dir exists
    os.makedirs(COVERAGE_DIR, exist_ok=True)
    os.environ['COVERAGE_PROCESS_START'] = os.path.join(REPO_ROOT,".coveragerc")
    load_dotenv()
    capture = False
    script_env = os.environ.copy()
    # we create a coverage file for each run
    script_env['COVERAGE_FILE'] = os.path.join(COVERAGE_DIR, ".coverage." + script.replace(os.sep,"_")) 
    basepath = os.path.dirname(script)
    script_only = os.path.basename(script).replace(".py","")
    process = subprocess.run([PYTHON,"-m",script_only], env=script_env,cwd=basepath, capture_output=capture)
    return process