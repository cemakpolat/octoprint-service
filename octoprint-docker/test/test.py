"""
@author: Cem Akpolat
@created by cemakpolat at 2021-10-06
"""
import  subprocess
process = subprocess.run(['echo', 'Even more output'],
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
print(process.stdout)

import subprocess
process = subprocess.Popen(['echo', 'More output'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr

import os
stream = os.popen('docker-compose up -d')
output = stream.read()
print(output)

os.system('ls -l')
