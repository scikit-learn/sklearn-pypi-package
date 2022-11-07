import os
import sys
from datetime import datetime, MAXYEAR
from collections import namedtuple

from setuptools import setup
from setuptools.command.install import install


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()


def get_brownout_schedule():
    all_start_dates = [datetime(2022, 12, 1)] + [
        datetime(2023, 2 * i, 1) for i in range(1, 7)
    ]
    date_in_the_far_future = datetime(MAXYEAR, 12, 31, 23, 59, 59)
    all_end_dates = all_start_dates[1:] + [date_in_the_far_future]
    all_check_functions = [
        lambda dt: dt.minute < 5,
        lambda dt: dt.minute < 10,
        lambda dt: dt.minute < 15,
        lambda dt: (dt.minute < 10) or (30 <= dt.minute < 40),
        lambda dt: (dt.minute < 15) or (30 <= dt.minute < 45),
        lambda dt: (dt.minute < 20) or (30 <= dt.minute < 50),
        lambda dt: True,
    ]

    CheckedDatetimeWindow = namedtuple(
        "CheckedDatetimeWindow", "start_datetime end_datetime check_function"
    )
    brownout_schedule = [
        CheckedDatetimeWindow(*each)
        for each in zip(all_start_dates, all_end_dates, all_check_functions)
    ]

    return brownout_schedule


def maybe_raise_error(checked_datetime):
    accept_deprecated_sklearn_package_install = os.environ.get(
        "SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL", "use-brownout-schedule"
    )
    accept_deprecated_sklearn_package_install = (
        accept_deprecated_sklearn_package_install.lower()
    )

    if accept_deprecated_sklearn_package_install == "true":
        return

    if accept_deprecated_sklearn_package_install == "false":
        raise SystemExit(
            "Refusing to install the deprecated sklearn package, "
            "because SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=False is set"
        )

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
            "",
            "If the previous advice does not cover your use case, feel free to report it at",
            "https://github.com/scikit-learn/sklearn-pypi-package/issues/new",
        ]
    )

    brownout_schedule = get_brownout_schedule()
    for start_date, end_date, check_function in brownout_schedule:
        if (start_date <= checked_datetime < end_date) and check_function(
            checked_datetime
        ):
            raise SystemExit(error_message)


if __name__ == "__main__":
    # We allow python setup.py sdist to always work to be able to create the
    # sdist and upload it to PyPI
    sdist_mode = len(sys.argv) == 2 and sys.argv[1] == "sdist"

    if not sdist_mode:
        # environment variable for test purposes
        datetime_str = os.getenv("SKLEARN_DEPRECATED_SKLEARN_CHECKED_DATETIME", None)
        if datetime_str is None:
            checked_datetime = datetime.now()
        else:
            checked_datetime = datetime.fromisoformat(datetime_str)

        maybe_raise_error(checked_datetime)

    setup(
        description="deprecated sklearn package, use scikit-learn instead",
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        name="sklearn",
        version="0.0.post1",
    )
