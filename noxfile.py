"""
Nox definitions for tests, docs, and linting
"""

import nox


COVERAGE_FAIL = 90
ERROR_ON_GENERATE = True
locations = "canu", "tests", "noxfile.py"
nox.options.sessions = "tests", "lint", "cover"


@nox.session(python="3")
def tests(session):
    """Default unit test session.
    This is meant to be run against any python version intended to be used.
    """
    # Install all test dependencies, then install this package in-place.
    path = "tests"
    session.install("-r", "requirements-test.txt")
    session.install("-e", ".")

    if session.posargs:
        path = session.posargs[0]

    # Run pytest against the tests.
    session.run(
        "pytest",
        "--quiet",
        "--cov=canu",
        "--cov=tests",
        "--cov-append",
        "--cov-report=",
        "--cov-fail-under={}".format(COVERAGE_FAIL),
        path,
        *session.posargs
    )


@nox.session(python="3")
def lint(session):
    """
    Run flake8 linter and plugins.
    """
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python="3")
def black(session):
    """
    Run Black, the uncompromising Python code formatter.
    """
    args = session.posargs or locations
    # exclude = "(/bin, /lib)"
    exclude = """
    ^/(
    (
        canu/lib
        | canu/bin
    )
    )
    """
    session.install("black")
    session.run("black", "--exclude", exclude, *args)


@nox.session(python="3")
def cover(session):
    """
    Run the final coverage report.
    """
    session.install("coverage", "pytest-cov")
    session.run(
        "coverage", "report", "--show-missing", "--fail-under={}".format(COVERAGE_FAIL)
    )
    session.run("coverage", "erase")
