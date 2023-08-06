# WSCheck
[![PyPi](https://img.shields.io/badge/download-PyPi-green.svg)](https://pypi.org/project/wscheck/)
[![Build](https://travis-ci.org/andras-tim/wscheck.svg?branch=master)](https://travis-ci.org/andras-tim/wscheck/branches)
[![Docs](https://readthedocs.org/projects/wscheck/badge/?version=latest)](http://wscheck.readthedocs.org/en/latest/)
[![DependencyStatus](https://requires.io/github/andras-tim/wscheck/requirements.svg?branch=master)](https://requires.io/github/andras-tim/wscheck/requirements/?branch=master)
[![CodeQuality](https://api.codacy.com/project/badge/Grade/448b73826c97497d8bf0e2970cba1156)](https://www.codacy.com/app/andras-tim/wscheck)
[![Coverage](https://coveralls.io/repos/andras-tim/wscheck/badge.svg?branch=master&service=github)](https://coveralls.io/r/andras-tim/wscheck?branch=master&service=github)
[![License](https://img.shields.io/badge/license-GPL%203.0-blue.svg)](https://github.com/andras-tim/wscheck/blob/master/LICENSE)

[WSCheck](https://github.com/andras-tim/wscheck) is a static analysis tool for whitespaces.


## Installation

``` sh
pip install wscheck
```

## Usage

**Check multiple files:**

``` sh
wscheck orange.sh pineapple.xml kiwi.js
```

**Exclude rules:**

``` sh
wscheck --exclude WSC002 --exclude WSC003 orange.sh
```

**Get list of available rules:**

``` sh
wscheck --list-rules
```

For details about rules, see [Rules](http://wscheck.readthedocs.io/en/latest/rules/index.html)

**Write CheckStyle output too:**

``` sh
wscheck --checkstyle results.xml pineapple.xml
```


## Example

``` sh
wscheck examples/multiple_problems.py
```
```
In examples/multiple_problems.py line 2:
class LabelPrinter:
^-- WSC007: File begins with newline

In examples/multiple_problems.py line 6:
        self.print_to_pdf()
                           ^-- WSC002: Tailing whitespace

In examples/multiple_problems.py line 9:
   def __generate_pdf(self):
   ^-- WSC003: Indentation is not multiple of 2

In examples/multiple_problems.py line 10:
        pdf_generator = _LabelPdfGenerator()
                                            ^-- WSC001: Bad line ending '\r\n'

In examples/multiple_problems.py line 16:
--->--->os.makedirs(self.__cache_dir, exist_ok=True)
^-- WSC004: Indentation with non-space character

In examples/multiple_problems.py line 22:
        return os.path.join(self.__cache_dir, pdf_name)
                                                       ^-- WSC006: Too many newline at end of file (+1)
```

## Bugs

Bugs or suggestions? Visit the [issue tracker](https://github.com/andras-tim/wscheck/issues).


## Benchmark

* You can run a quick benchmark:

    ``` sh
    tox -- tests/performance --quick-benchmark
    ```

* You can run benchmarks and generate histogram for compare calls to each other:

    ``` sh
    tox -- tests/performance --benchmark-histogram
    ```

* You can run benchmarks and save results for later compare:

    ``` sh
    tox -- tests/performance --benchmark-save=foo
    ```

* You can run benchmarks and compare with the last saved result with fail treshold:

    ``` sh
    tox -- tests/performance --benchmark-histogram --benchmark-compare --benchmark-compare-fail=mean:5% --benchmark-sort=name
    ```

* You can run benchmarks and compare with the last saved result by groups:

    ``` sh
    tox -- tests/performance --benchmark-histogram --benchmark-compare --benchmark-group-by=func
    
    tox -- tests/performance --benchmark-histogram --benchmark-compare --benchmark-group-by=name
    ```
