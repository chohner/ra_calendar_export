from ra_calendar_export import __version__
import black
from click.testing import CliRunner
from pathlib import Path


def test_version():
    assert __version__ == "0.1.0"


def test_lint():
    code_root = Path(__file__).parent.parent
    runner = CliRunner()
    result = runner.invoke(
        black.main,
        [str(code_root / "ra_calendar_export"), str(code_root / "tests"), "--check"],
    )
    assert result.exit_code == 0, (
        result.output + "\n\nFix by running 'poetry run lint'!\n"
    )
