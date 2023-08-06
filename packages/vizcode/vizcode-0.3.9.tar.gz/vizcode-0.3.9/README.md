# VizCode

VizCode is a command line tool for visualizing codebases as directed graphs. It utilizes static analysis to parse through your code to detect any definitions and references, which are then represented as nodes and edges respectively in a graph. Furthermore, the graph will be visualized on a web browser once the code files have been parsed. VizCode only supports the Python language at the moment.

![](https://i.ibb.co/28S6ZFx/vizcode-screenshot.png)

Please note that VizCode is run locally and will never send your code, repository names, file names, or any other specific code data to any location outside of your local machine. Additionally, VizCode is not able to run on Windows unless you download the Ubuntu shell. For more information about VizCode visit our [website](https://vizcode.dev).

## Installation

You can install VizCode from [PyPI](https://pypi.org/project/vizcode/):

    pip install vizcode

VizCode is supported on Python 3.7 and above.

## How to use

To run VizCode on a codebase, simply call the program:

    $ vizcode -p [ENTER A DIRECTORY PATH]

Since VizCode only works on Python code, it will ignore any files without the .py file extension. If your code uses any dependencies that are not installed in your default environment, then you can specify an environment path:

    $ vizcode -p [ENTER A DIRECTORY PATH] -e [ENTER AN ENVIRONMENT PATH]

If you would like VizCode to ignore test files, then you can add an additional argument:

    $ vizcode -p [ENTER A DIRECTORY PATH] -t [ENTER PATH OF TEST FILES]
