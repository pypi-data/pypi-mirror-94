# PKDGrav to MATLAB converter
Converts pkdgrav binary output (ss) to matlab readable files.

## Install
 * Install directly from pip or run `pip install .` inside the source directory

## Usage 
 * Execute in shell: `ss2mat <filename>`
 * If you add `--si` the data is converted into SI-units (sm-kg, au-m, yr/2pi-s, sm/au^3-g/cm^3).
 * If you add `--endianess` you can specify the endianess of the input data (depends on the platform of the file creator).
 * Follow the instructions.

## Notes for developers

### Versioning
 * Versioning is done using git.
 * The primary repository is at [github.com](https://github.com/cstatz/pkdgrav2matlab)

### Coding style
 * We try to adhere to [Python PEP8](https://www.python.org/dev/peps/pep-0008/)
 * If you use PyCharm: activate the PEP8 compliance check
