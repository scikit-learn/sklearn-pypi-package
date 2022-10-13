import os
from datetime import datetime, MAXYEAR
from dateutil.relativedelta import relativedelta
from setuptools import setup


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()


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

    start_date = datetime(2022, 11, 1)
    all_start_dates = [start_date + relativedelta(months=2 * i) for i in range(7)]
    date_in_the_far_future = datetime(MAXYEAR, 12, 31, 23, 59, 59)
    all_end_dates = all_start_dates[1:] + [date_in_the_far_future]
    all_check_functions = [
        lambda dt: dt.minute < 5,
        lambda dt: dt.minute < 10,
        lambda dt: dt.minute < 15,
        lambda dt: (dt.minute < 10) or (30 < dt.minute < 40),
        lambda dt: (dt.minute < 15) or (30 < dt.minute < 45),
        lambda dt: (dt.minute < 20) or (30 < dt.minute < 50),
        lambda dt: True,
    ]
    brownout_schedule = zip(all_start_dates, all_end_dates, all_check_functions)

    error_message = "\n".join(
        [
            "The 'sklearn' PyPI package is deprecated, use 'scikit-learn' ",
            "rather than 'sklearn' for pip commands. ",
            "",
            "The brownout schedule for sklearn deprecation can be found at ",
            "https://github.com/scikit-learn/sklearn-pypi-package#brownout-schedule",
            "",
            "Here is how to fix this error in the main use cases:",
            "- use 'pip install scikit-learn' rather than 'pip install sklearn'",
            "- replace sklearn by scikit-learn in your pip requirements files",
            "  (requirements.txt, setup.py, setup.cfg, Pipfile, etc ...)",
            "- if the sklearn package is used by one of your dependencies, ",
            "  it would be great if you take some time to track which pakage uses ",
            "  sklearn instead of scikit-learn and report it to their issue tracker",
            "- as last resort, set the environment variable ",
            "  SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True to avoid this error",
            "",
            "If the previous advice does not cover your use case, feel free to report it at:",
            "https://github.com/scikit-learn/sklearn-pypi-package/issues/new",
        ]
    )
    for start_date, end_date, check_function in brownout_schedule:
        if (start_date <= checked_datetime < end_date) and check_function(
            checked_datetime
        ):
            raise SystemExit(error_message)


def main():
    now = datetime.now()
    now = datetime(2022, 11, 1)
    maybe_raise_error(now)

    setup(
        description="deprecated sklearn package, use scikit-learn instead",
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        name="sklearn",
        version="0.1.0a1",
    )


if __name__ == "__main__":
    main()
