import subprocess

from avocado import Test

from integration_tests.build import build_image
from integration_tests.run import extract_image


class SleepTest(Test):
    pipeline = "timezone.json"
    output_image = "timezone.tar.xz"

    @classmethod
    def setUp(self) -> None:
        build_image(self.pipeline)

    def test_timezone(self):
        with extract_image(self.output_image) as extract_dir:
            ls = subprocess.run(["ls", "-l", "etc/localtime"], cwd=extract_dir, check=True, stdout=subprocess.PIPE)
            ls_output = ls.stdout.decode("utf-8")
            assert "Europe/Prague" in ls_output
