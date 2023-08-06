# pymobility
###### Work done by South Asia Poverty Team, The World Bank

_pymobility_ is the Python package built on top of PySpark API, which faciliates big data processing. This package has
several sub-packages and modules for quantifying mobility and migration from raw GPS data. The package takes _delta_
formatted geo-tagged raw dataset and generates various datasets like Origin Destination matrix and net migration figures,
and various statistics like average records in a time-period, average devices registered in a time period, etc.

_pymobility_ has three sub-packages: _odm_, _stm_, and _eda_. _odm_ is used for generating origin-destination figures.
_stm_ helps to quantify short term migration depending on whatever definition we use for short term migrants. The _stm_
sub-package is made modular, and there are a number of parameters which can be set according to the definition of short
term migrant used. Another sub-package, _eda_, helps to do exploratory data analysis. We can get statistics like average
devices in some time-period, or average records in some time-period, etc. More documentation about the individual
sub-packages is done on the sub-package README file itself.

## Dependencies
As the package is built on top of _PySpark API_, _Python_ API for _Spark_ (or _PySpark API_) should be installed. The code is
well tested on _Python 3.6_, so users are encouraged to have _Python 3.6+_ version.

Other _Python_ packages used herein are _Pandas_.

## Installation

Both _pyspark_ and _pandas_ can be installed using _pip_. The commands for them are given below:

```
pip install pandas
pip install pyspark
```
More details about _pyspark_ can be found [here](https://github.com/apache/spark/tree/master/python).

## Usage
This package can be used for quantifying mobility and migration from geo-taggged raw _delta_ files. It facilitates
following features.
1. Origin Destination Matrix (OD matrix): Details about use of this library for quantifying origin-destination movement
can be found in the [README.md](mobility/odm/README.md) file inside the _odm_ sub-package itself.
   
2. Short Term Migration: This type of migration is quantified using _stm_ sub-package, which facilitates flexibility in
short term migrants' definition with the help of different parameters like away time period required, definition of 
   home, etc.
   
3. Exploratory Data Analysis: The exploratory data analysis can be done using the _eda_ sub-package. Under _eda_
commuter aggregates and mobility summary can be quantified.