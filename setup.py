import os
import sys
import warnings

from setuptools import setup


with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


def likely_error():
    accept_deprecated_sklearn_package_install = os.environ.get(
        "SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL", "unset"
    )
    accept_deprecated_sklearn_package_install = (
        accept_deprecated_sklearn_package_install.lower()
    )

    if accept_deprecated_sklearn_package_install == "true":
        return

    error_message = "\n".join(
        [
            "The 'sklearn' PyPI package is deprecated, use 'scikit-learn'",
            "rather than 'sklearn' for pip commands. ",
            "",
            "Here is how to fix this error in the main use cases:",
            "- use 'pip install scikit-learn' rather than 'pip install sklearn'",
            "- replace 'sklearn' by 'scikit-learn' in your pip requirements files",
            "  (requirements.txt, setup.py, setup.cfg, Pipfile, etc ...)",
            "- if the 'sklearn' package is used by one of your dependencies,",
            "  it would be great if you take some time to track which package uses",
            "  'sklearn' instead of 'scikit-learn' and report it to their issue tracker",
            "- as a last resort, set the environment variable",
            "  SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True to avoid this error",
            "",
            "More information is available at",
            "https://github.com/scikit-learn/sklearn-pypi-package",
        ]
    )

    raise SystemExit(error_message)


if __name__ == "__main__":
    # We allow python setup.py sdist to always work to be able to create the
    # sdist and upload it to PyPI
    sdist_mode = len(sys.argv) == 2 and sys.argv[1] == "sdist"

    if not sdist_mode:
        likely_error()

    setup(
        description="deprecated sklearn package, use scikit-learn instead",
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        name="sklearn",
        version="0.0.post12",
    )
