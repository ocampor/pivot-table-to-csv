# Pivot Table to CSV

*This repository takes a `*.xslx` that contains a Pivot Table with hidden external source data and converts the pivot cache into a text file with `,` separated values. It takes into account files that are too big to be in memory and handles this situation by dividing the original data into `n` batches.*

## Documentation
### Methodology
This codes unzips the `xlsx` file and extracts the data contained in the `pivotCacheRecords{0}.xlm` files. The pivot cache records are parsed and organized into a `,` separated values.  

## Getting Started
### Prerequisites
1. python 3.6 and pip

### Installing
1. Clone the project from ocampor/pivot-table-to-csv
1. Install python 3.6 and pip
1. Create a virtual environtment `virtualenv --python=python3.6 .venv` and source it `source .venv/bin/activate`
1. Install python requirements `pip install -r requirements.txt`

## Run code
You can run the code by executing `python main.py`. The options are the following:
1. `-f` or `--file` a required option that specifies the file to convert.
1. `-o` or `--output` optional option that specifies the desired output file name.
1. `-n` or `--nchunks` the number or pieces to split original file before converting. It is recommended to split the file into 5 pieces for excel files of size 100 mb. The latter recommendation for equipments with 16 gb of RAM. 
1. `-v` or `--verbose` activates DEBUG level of logging.

## Running the tests
1. Run `py.test`

## Deployment
To be included

## Contributing
When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent.
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors
* **Ricardo Ocampo** - *Initial work* - [ocampor](https://github.com/ocampor)
