# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvdastwrapper']

package_data = \
{'': ['*']}

install_requires = \
['cvdast']

entry_points = \
{'console_scripts': ['cvdast-wrapper = cvdastwrapper.entry:main']}

setup_kwargs = {
    'name': 'cvdastwrapper',
    'version': '1.48.7',
    'description': 'This is a wrapper around CVDAST',
    'long_description': '\n--------- ReadMe:\n\n1. About ----\n\n* Python Runtime and Package Installation\nFirst of it, it is assumed that python3 and pip3 are installed. And\ncvdast package is installed by pip3. The python3 command can sometimes\njust be "python" if your default python installation is version 3 or above.\nPlease run "python --version" to find out. If you are running python 3 or above\nby default, please simply substitute the "python3" commands in examples provided\nin the remainder of this document.\n\nTo ensure cvdast is up-to-date, please run:\n   pip3 install -U cvdast\n\n* Test Directory\nThis self-contained package, when decompressed/unzipped, should be the\ntest directory from which you can generate fuzz data based on the specs\nand then run. Please feel free to rename the test directory. The\nsubdirectory structure is important for the test run. All files generated\nwill be put under the test directory.\n\n* Config: \nThere will be information such as the URL of your test application (API endpoint),\nthe list of the fuzz attacks to try etc. The runconfig.py file contains\nall of the custom variables one needs to change. Current values are provided\nas examples. \n\nAfter a complete runall.py run(details in sections below), the summary.html\nfile will contain pointers to all the test results. In addition, a file called\nfordev-apis.csv is generated. This is a highlevel summary for consumption of a\ndev team. It highlight just the API endpoints that seem to "fail" the test, ie.\nresponding positively instead of rejecting the fuzz calls. Please feel free to\nimport such CSV report to a spreadsheet. \n\nThe test results are stored in\n    results\n    results/perapi\n    results/perattack\n\nTest can run for a long time, so one can adjust the spec and the\ncollection of attacks in runall.py to stage each run. Test results\nof different test will not over-write each other. You can regenerate\ntest report after the test run.\n\nauth.py must be in this directory\ncv_config_oc.yaml is hardcoded in fuzzallspecs. Must be present\n\n2. Generate fuzzing test for all the specs ----\n\nWith a given cvdast version and a set of specs, you need to only run\nthis once.\n\npython3 fuzzallspecs.py \n\nwill fuzz all specs, run it with "--help" will let you know an optional input\nwhich is the spec directory, default is "specs".\n\nA successfully run fuzzallspecs will generate as output a list of spec\ntitle names (taken from the spec\'s title) that can be used to update runall.py\nlist for test control (later 4. Control test)\n\nA specs directory containing all .json app spec is used to store the\nspecs for testing. \n\n3. Running Tests -----------\n\nOne can run this script: \n\n python3 runall.py\n\nAfter fuzzallspecs.py, it will run both runperattack and runperapi to generate\ntwo sets of results. It takes a "regen" argument. Regen will tells it not to\nrun the long test, but just run the cloudVectorDAST.generate_fuzz_report to\nagain generate the report (it copies the saved report.json from results\ndirectory)\n\nIt creates a summary.html in the test. It contains tables allowing convenient\naccess to all the reports\n\nResults are saved in a directory called results\n\n  results\n    results/perapi\n    results/perattack\n\nAfter the runall call, you can find subdirectories with the Spec names under\neach of these results directories.\nThere are .html files that are the report html pointed to by the summary.\n\nUnder the perapi directory there are files that are named after the API\nname (chopped from the test directory long "for_fuzzing.py" name). The\nreport.json of the test run is saved with <apiname>-report.json\n\nSame naming convention goes for perattack reports.\n\n\npython3 runperapi.py\npython3 runperattack.py\n\nCan be run seperately to test. They will update the test results but they won\'t\nupdate summary.html. \n\n\n4 Controlling Spec and Attack for testing -------\n\nIn runall.py, there are two lists\n(and two corresponding full list for reference).\n\nThe test can take multiple hours, or even a day if the full list is used.\n\n\napispeclist=["CpmGateway",\n          "TelemetryGateway"]\n\nfuzzattacklist = [\'sql-injection/detect\']\n\nfuzzattacklist = [\'control-chars\', \'string-expansion\', \'server-side-include\',\n                  \'xpath\', \'unicode\', \'html_js_fuzz\', \'disclosure-directory\',\n                  \'xss\', \'os-cmd-execution\', \'disclosure-source\',\n                  \'format-strings\', \'xml\', \'integer-overflow\',\n                  \'path-traversal\', \'json\', \'mimetypes\', \'redirect\',\n                  \'os-dir-indexing\', \'no-sql-injection\', \'authentication\',\n                  \'http-protocol\', \'business-logic\',\n                  \'disclosure-localpaths/unix\',\n                  \'file-upload/malicious-images\',\n                  \'sql-injection/detect\',\n                  \'sql-injection/exploit\',\n                  \'sql-injection/payloads-sql-blind\']\n\'\'\'\n',
    'author': 'Bala Kumaran',
    'author_email': 'balak@cloudvector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
