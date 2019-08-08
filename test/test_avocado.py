import subprocess
import time

from avocado import Test

# from integration_tests import rel_path
# from integration_tests.build import run_osbuild
# from integration_tests.run import extract_image


class SleepTest(Test):
    name = "timezone"
    pipeline = "timezone.json"
    output_image = "timezone.tar.xz"

    @classmethod
    def setUpClass(cls) -> None:
        # run_osbuild(rel_path(f"pipelines/{cls.pipeline}"))
        pass

    def test_timezone(self):
        # with extract_image(self.output_image) as extract_dir:
        #     ls = subprocess.run(["ls", "-l", "etc/localtime"], cwd=extract_dir, check=True, stdout=subprocess.PIPE)
        #     ls_output = ls.stdout.decode("utf-8")
        #     assert "Europe/Prague" in ls_output
        pass
