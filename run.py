import sys
from pathlib import Path
from getpass import getpass

from click.testing import CliRunner

def ics_export():
    from ra_calendar_export import main  # importing at top of file would screw up coverage
    username = input("username:")
    password = getpass("password (only for private profiles):")
    main.ics_file_from_profile(username, password)

def lint():
    try:
        import black
    except ModuleNotFoundError as e:
        print("Linting is not available without Black installed, exiting.")
        sys.exit(1)
    code_root = Path(__file__).parent
    runner = CliRunner()
    result = runner.invoke(
        black.main,
        ["run.py", f"{code_root}/ra_calendar_export", f"{code_root}/tests"],
        mix_stderr=True,
        color=True
    )
    print(result.stdout)
    sys.exit(0) if result.exit_code == 0 else sys.exit(1)

def test():
    try:
        import pytest
    except ModuleNotFoundError:
        print("Testing is not available without pytest installed, exiting.")
        sys.exit(1)
    test_result = pytest.main(['--cov=ra_calendar_export', '--cov-report', 'term-missing'])
    sys.exit(0) if test_result == pytest.ExitCode.OK else sys.exit(1)
