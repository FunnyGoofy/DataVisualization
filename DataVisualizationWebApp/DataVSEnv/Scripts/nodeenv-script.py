#!C:\Workplace\Projects\PythonProjects\PythonTest\DataVisualization\DataVisualizationWebApp\DataVSEnv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'nodeenv==1.3.2','console_scripts','nodeenv'
__requires__ = 'nodeenv==1.3.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('nodeenv==1.3.2', 'console_scripts', 'nodeenv')()
    )