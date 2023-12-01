# ⚠️⚠️⚠️ Summary ⚠️⚠️⚠️

⚠️⚠️⚠️ The **`sklearn` PyPI package is deprecated use `scikit-learn` instead** ⚠️⚠️⚠️

# How to fix the error for the main use cases

- use `pip install scikit-learn` rather than `pip install sklearn`
- replace `sklearn` by `scikit-learn` in your pip requirements files
  (`requirements.txt`, `setup.py,` `setup.cfg`, `Pipfile`, etc ...)
- if the `sklearn` package is used by one of your dependencies
  it would be great if you take some time to track which package uses
  `sklearn` instead of `scikit-learn` and report it to their issue tracker
- as a last resort, set the environment variable
  `SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True` to avoid this error

# Reason for the deprecation

`sklearn` package on PyPI exists to prevent malicious actors from using the
`sklearn` package, since `sklearn` (the import name) and `scikit-learn` (the
project name) are sometimes used interchangeably. `scikit-learn` is the actual
package name and should be used with pip, e.g. for:
- pip commands: `pip install scikit-learn`
- pip requirement files (`requirements.txt`, `setup.py,` `setup.cfg`,
  `Pipfile`, etc ...)

At the time of writing (October 2022) `sklearn` downloads is about 1/5 of the
`scikit-learn` downloads on PyPI so a lot of people are using it.

There are some edge cases with the way the PyPI `sklearn` package is
implemented:
- `pip install sklearn==1.1.3` will say that the 1.1.3 version does not exist,
  which is confusing. The only available version at the time of writing of
  `sklearn` is 0.0.
- `pip uninstall sklearn` will actually not uninstall `scikit-learn`, you can
  still do `import sklearn` afterwards
- it can be confusing to have both `sklearn` and `scikit-learn` in the `pip
  list` output, prompting questions like "why do I have scikit-learn 1.1.3 and
  sklearn 0.0, and what does it even mean"?

# Historical brownout schedule (from 2022-12-01 to 2023-12-01)

Starting 2023 December 1st, trying to install the `sklearn` PyPI package raises
an error.

The table shows the historical brownout schedule that was used between 2022
December 1st and 2023 December 1st, in order to get people aware of the
deprecation and give them some time to adapt. During these dates and time
windows, an exception was raised if you attempted to install the `sklearn`
package from PyPI.

| Dates                                 | Window(s)                      |
|---------------------------------------|--------------------------------|
| 2022 December 1st - 2023 January 31st | :00-:05 every hour             |
| 2023 February 1st - March 31st        | :00-:10 every hour             |
| 2023 April 1st - May 31st             | :00-:15 every hour             |
| 2023 June 1st - July 31st             | :00-:10 and :30-:40 every hour |
| 2023 August 1st - September 30th      | :00-:15 and :30-:45 every hour |
| 2023 October 1st - November 30th      | :00-:20 and :30-:50 every hour |
| 2023 December 1st onwards             | always raise an exception      |
