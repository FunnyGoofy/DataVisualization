#!C:\Workplace\Projects\PythonProjects\PythonTest\DataVisualization\DataVisualizationWebApp\DataVSEnv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'webruntime==0.5.3','console_scripts','webruntime'
__requires__ = 'webruntime==0.5.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('webruntime==0.5.3', 'console_scripts', 'webruntime')()
    )
