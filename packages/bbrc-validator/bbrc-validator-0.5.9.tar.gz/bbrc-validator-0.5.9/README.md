bbrc-validator 
==============

[![pipeline status](https://gitlab.com/bbrc/xnat/bbrc-validator/badges/master/pipeline.svg)
](https://gitlab.com/bbrc/xnat/bbrc-validator/commits/master)
[![coverage report](https://gitlab.com/bbrc/xnat/bbrc-validator/badges/master/coverage.svg)
](https://gitlab.com/bbrc/xnat/bbrc-validator/commits/master)
[![python](https://img.shields.io/pypi/pyversions/bbrc-validator.svg)
](https://pypi.org/project/bbrc-validator)
[![pypi](https://img.shields.io/pypi/v/bbrc-validator.svg)
](https://pypi.org/project/bbrc-validator)

<p align="center">
  <a href="#main-concepts">Main Concepts</a> •
  <a href="#commands">Commands</a> •
  <a href="#example">Examples</a> •
  <a href="#install">Install</a> •
  <a href="#contributing">Contributing</a>
</p>

**bbrc-validator** is a Python-based software package that performs automatic quality 
assessment of neuroimaging datasets and their processing derivatives, through 
collections of "checkpoints". 
**bbrc-validator** is built on two core concepts: _Tests_ and _Validators_.

- A **Test** checks a specific trait from a given resource (either an imaging 
  session or a single scan). It asks a specific question whose answer can be 
  either `True` or `False` (eg. _"Does this MRI scan have a conversion to NIfTI 
  available?"_). As such, _Tests_ may be seen as [unit tests
  ](https://en.wikipedia.org/wiki/Unit_testing).  A _Test_ class is defined by two 
  attributes (`passing` and `failing`) that refer to two "real-life" cases (one 
  expected to pass the _Test_ and another expected to fail it). In addition, these 
  attributes are systematically used by the [CI
  ](https://en.wikipedia.org/wiki/Continuous_integration) testing.
  
- A **Validator** is a collection of **Test** objects that may be executed against 
  any [XNAT](https://www.xnat.org/) imaging resource (by referring to their experiment 
  identifiers). Running a _Validator_ on a given experiment takes its associated 
  set of tests, runs them sequentially and collects their results in a JSON object. 
  A human-readable report can be  generated (as a PDF document) with the results
  of the whole procedure.

Main Concepts 
-------------

- __Test__:
                                
   ```python
    class MyTest():
        """ Test functionality description """
        passing = 'PASSING_CASE_ID'
        failing = 'FAILING_CASE_ID'
        
        def run():     # executes the Test logic and returns some Results
            return Results(has_passed=test_outcome, data=some_data)  
        def report():  # provides a human-readable version of Results data
   ```
                 
- __Validator__:                 
  
   ```python
    class MyValidator():
        def __init__():
            self.tests = [MyTest, ...]        
        
        def run():     # runs all Tests sequentially             
        def dump():    # compiles all Test results in a single JSON object    
        def report():  # generates a human-readable PDF report based on the results
   ```
               
- __Result__: Represents the outcome from the execution of a _Test_. It includes
              a boolean attribute `has_passed` (representing the outcome of _Test_
              execution) and some additional `data` object (optionally used for 
              storing contextual information from the execution).
  
Commands
--------

### `run_validator.py`

Executes the specified _Validator_ against a given image resource (a.k.a XNAT 
_experiment_) and generates (a) a JSON object with the results of all the Tests 
and (b) a human-readable PDF report.
```
usage: run_validator.py [-h] --config CONFIG --experiment EXPERIMENT
                        [--validator VALIDATOR] --output OUTPUT [--verbose]

Run a validator against an experiment

optional arguments:
  -h, --help                             show this help message and exit
  --config CONFIG, -c CONFIG             XNAT configuration file
  --experiment EXPERIMENT, -e EXPERIMENT XNAT experiment unique identifier
  --validator VALIDATOR, -v VALIDATOR    Validator name (default:ArchivingValidator)
  --output OUTPUT, -o OUTPUT             PDF file to store the report
  --verbose, -V                          Display verbosal information (optional)
```

### `validation_scores.py`
 
Given a specific type of _Validator_, collects all results available in an XNAT 
instance and compiles them in a CSV file.  
```
usage: validation_scores.py [-h] --config CONFIG --version VERSION
                            [--validator VALIDATOR] --output OUTPUT 
                            [--project PROJECT] [--verbose]

Compile validation scores

optional arguments:
  -h, --help                    show this help message and exit
  --config CONFIG               XNAT configuration file
  --version VERSION, -v VERSION Filter specific version
  --validator VALIDATOR         Validator name (default:ArchivingValidator)                      
  --output OUTPUT, -o OUTPUT    CSV output file
  --verbose, -V                 Display verbosal information (optional)
```

Enables the creation of tables such as the following example obtained from
`ArchivingValidator` (table trimmed to fit the dimensions of the page).

_Tests_ included:

1. HasUncompressedPixelData
2. HasCorrectSequences
3. HasBvecBval
4. IsClassicDICOM
5. HasDuplicatedSequences
6. HasNifti
7. HasPhilipsPrivateTags
8. IsStudyDescriptionCorrect

<table border="1" cellpadding="0" cellspacing="0" dir="ltr">
	<tbody>
		<tr>
			<td>Tests</td>
			<td><pre>#1</pre></td>
			<td><pre>#2</pre></td>
			<td><pre>#3</pre></td>
			<td><pre>#4</pre></td>
			<td><pre>#5</pre></td>
			<td><pre>#6</pre></td>
			<td><pre>#7</pre></td>
			<td><pre>#8</pre></td>
		</tr>
		<tr>
			<td>Sums</td>
			<td>11</td>
			<td>11</td>
			<td>0</td>
			<td>11</td>
			<td>11</td>
			<td>6</td>
			<td>0</td>
			<td>11</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00211</td>
			<td> ![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td> ![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td> ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00210</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00213</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00212</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00196</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00214</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00217</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00216</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00219</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00218</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
		<tr>
			<td>BBRCDEV_E00198</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
			<td>![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)</td>
			<td>![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)</td>
		</tr>
	</tbody>
</table>

Examples
--------

#### Create a Validator and review the list of its Tests
1. Set a [pyxnat connection
   ](https://pyxnat.github.io/pyxnat/tutorial.html#setting-up-a-connection)
   to the XNAT instance hosting the data requiring validation.     
2. Create an instance of `SPM12SegmentValidator`, a _Validator_ for segmentations
   produced using [SPM12 Segment](https://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#page=45).
3. Print out a list of included tests.     
```python
import pyxnat
intf = pyxnat.Interface(config='.xnat.cfg')

from bbrc.validation import SPM12SegmentValidator
spmv = SPM12SegmentValidator(lut={}, xnat_instance=intf)

print('{} tests (`{}`):'.format(spmv.__class__.__name__, spmv.version))
spmv.tests
```
    SPM12SegmentValidator tests (`d6ca22c1`):
    
    [<bbrc.validation.processing.spm.HasCorrectNumberOfItems at 0x273dee24e88>,
     <bbrc.validation.processing.spm.HasCorrectItems at 0x273dee247c8>,
     <bbrc.validation.processing.spm.HasCorrectSPMVersion at 0x273dda8f4c8>,
     <bbrc.validation.processing.spm.HasCorrectMatlabVersion at 0x273dee28848>,
     <bbrc.validation.processing.spm.HasCorrectOSVersion at 0x273dee287c8>,
     <bbrc.validation.processing.spm.SPM12SegmentSnapshot at 0x273dee249c8>,
     <bbrc.validation.processing.spm.HasNormalSPM12Volumes at 0x273dee28788>,
     <bbrc.validation.processing.spm.SPM12SegmentExecutionTime at 0x273dee28bc8>]

#### Run `SPM12SegmentValidator` against an MRI session,  
```python
spmv.run('XNAT_E00001')
```

    2021-02-04 12:12:54,635 - root - INFO - Running <bbrc.validation.processing.spm.HasCorrectNumberOfItems object at 0x00000273DEE24E88>
    2021-02-04 12:12:54,964 - root - ERROR - XNAT_E00001 has 15 items (different from 16)
    2021-02-04 12:12:55,572 - root - INFO - Running <bbrc.validation.processing.spm.HasCorrectItems object at 0x00000273DEE247C8>
    2021-02-04 12:12:56,120 - root - INFO - Running <bbrc.validation.processing.spm.HasCorrectSPMVersion object at 0x00000273DDA8F4C8>
    2021-02-04 12:12:56,592 - root - INFO - Running <bbrc.validation.processing.spm.HasCorrectMatlabVersion object at 0x00000273DEE28848>
    2021-02-04 12:12:56,782 - root - INFO - Running <bbrc.validation.processing.spm.HasCorrectOSVersion object at 0x00000273DEE287C8>
    2021-02-04 12:12:57,001 - root - INFO - Running <bbrc.validation.processing.spm.SPM12SegmentSnapshot object at 0x00000273DEE249C8>
    2021-02-04 12:13:04,997 - root - INFO - * Creating snapshots...
    2021-02-04 12:13:46,472 - root - INFO - Saved in /tmp/tmp3j664u27.png
    2021-02-04 12:13:46,515 - root - INFO - Running <bbrc.validation.processing.spm.HasNormalSPM12Volumes object at 0x00000273DEE28788>
    2021-02-04 12:13:50,552 - root - INFO - Running <bbrc.validation.processing.spm.SPM12SegmentExecutionTime object at 0x00000273DEE28BC8>

#### Collect results from `SPM12SegmentValidator` execution,
```python
import json 
result = spmv.dump()
json.loads(result)
```
    {'experiment_id': 'XNAT_E00001',
     'version': 'd6ca22c1',
     'generated': '2021-02-04, 12:13',
     'HasCorrectItems': {'has_passed': False,
      'data': ["Missing SPM12_SEGMENT items: ['pyscript_setorigin.m']."]},
     'HasCorrectSPMVersion': {'has_passed': True, 'data': []},
     'HasCorrectMatlabVersion': {'has_passed': True, 'data': []},
     'HasCorrectOSVersion': {'has_passed': True, 'data': []},
     'SPM12SegmentSnapshot': {'has_passed': True, 
      'data': ['/tmp/tmp3j664u27.png']},
     'HasNormalSPM12Volumes': {'has_passed': True,
      'data': ['Volumes: 773592.1702940931 524339.7480925963']},
     'SPM12SegmentExecutionTime': {'has_passed': True, 'data': ['0:07:15']}}

#### Generate a human-readable PDF report from the results,
```python
import tempfile
_,fp = tempfile.mkstemp(suffix='.pdf')
spmv.report(fp)
print('Report created: {}'.format(fp))

```
    Loading pages (1/6)
    Counting pages (2/6)                                               
    Resolving links (4/6)                                                       
    Loading headers and footers (5/6)                                           
    Printing pages (6/6)
    Done                                                                      
    
    Report created: '/home/jhuguet/notebooks/bbrc-validator/tmpcexwvwj5.pdf'

Install
-------

**bbrc-validator** can be installed via `pip`,
```bash
pip install bbrc-validator
```

`bbrc-validator` requires [wkhtmltopdf](http://wkhtmltopdf.org/) for PDF 
generation. A static build release (with QT patches) is recommended, see 
available releases 
[here](https://wkhtmltopdf.org/downloads.html) by OS/distribution.

On Ubuntu 18.04:
```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb
apt --fix-broken -y install
```
On CentOS 7:
```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.centos7.x86_64.rpm
yum -y  localinstall wkhtmltox-0.12.6-1.centos7.x86_64.rpm
```

Contributing
------------

**bbrc-validator** is still under active development. The currently included _Tests_ 
and _Validators_ have been tailored to the particular needs and context of the 
Barcelonaβeta Brain Research Center and as such might differ with the needs from 
other organizations.  
However, the software was designed with an aim towards genericity, modularity and 
reusability. Since all Tests are based upon the same template (eg. each of them 
being linked to XNAT data resources as test cases), this makes them virtually 
shareable across groups and makes **bbrc-validator** open to public contributions.

Contact us for details on how to contribute or open an issue to start a discussion.

[![BBRC](https://www.barcelonabeta.org/sites/default/files/logo-barcelona-beta_0.png)
](https://barcelonabeta.org/)