# Naive Tester

A simple testing system based on files. You provide a name of a script
to be tested and a folder containing files with arguments and reference
outputs. The app runs the script with the arguments from a file and compares
its result with that from the corresponding reference output file.
The following naming convention is applied:
each set of arguments is stored in the '.in' file, while the corresponding
output in the '.out' file, i.e., 'test_0.in' and 'test_0.out'.
Each pair must have identical names except for extensions.

## Installation
The Naive Tester can be installed from [PyPi](https://pypi.org/project/naive-tester/1.0.0/):
```
$ pip install naive-tester
```
The tester supports Python 3.6 and above. It is recommended to use virtual
environments for installation.

## How to use
Assume you created a python script some_app.py and want to test it. Your app
takes a string as an argument and outputs the length of that string to the console.
The application call might look like this:
```
$ python some_app.py input_string
$ 12
```
The first step is to prepare the tests, in this case, is to create a bunch of files.
Those with the '.in' extension must contain script arguments, i.e., 'input_string'
from the example above, and those with '.out' extension containing expected output,
i.e., '12'. The latter will be used for comparison with the script's output.
In other words, each pair of the files represents one test case.
```
some_app/
|
├── tests
|   ├── test_0.in
|   ├── test_0.out
|   ├── test_1.in
|   ├── test_1.out
|   ...
└── some_app.py
```
After the preparation step, you can run all the tests with the following command:
```
$ tester some_app.py tests
```
Example output is like the following:
```
Successfully run the some_app.py with tests/test_0.in
Failed run of the some_app.py with tests/test_1.in. The output should be 26.
```
It is possible to save the output to a file using a standard Linux technique:
```
$ tester some_app.py tests > test_report.txt 2>&1
```
Note ```2>&1``` because we are piping ```stderr```.

## Roadmap
For now, the Naive Tester can handle only scripts with a single argument.
This limitation needs to be overcome in the future version.

## Release History
* 1.0.0
    * 1.0.1 Minor bug fixes

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/FilippSolovev/naive-tester/blob/master/LICENSE) file for details
