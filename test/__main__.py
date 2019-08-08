import argparse
import logging
import os
import subprocess
import unittest

from test.integration_tests.run import extract_image
from test.integration_tests.test_case import IntegrationTestCase, IntegrationTestType
from test.integration_tests.config import *
from test.integration_tests import rel_path
from test.integration_tests.build import run_osbuild

logging.basicConfig(level=logging.getLevelName(os.environ.get("TESTS_LOGLEVEL", "INFO")))


def test_web_server_with_curl():
    cmd = ["curl", "-s", "http://127.0.0.1:8888/index"]
    logging.info(f"Running curl: {cmd}")
    curl = subprocess.run(cmd, capture_output=True)
    logging.info(f"Curl returned: code={curl.returncode}, stdout={curl.stdout.decode()}, stderr={curl.stderr.decode()}")
    assert curl.returncode == 0
    assert curl.stdout.decode("utf-8").strip() == "hello, world!"


def test_timezone(extract_dir):
    ls = subprocess.run(["ls", "-l", "etc/localtime"], cwd=extract_dir, check=True, stdout=subprocess.PIPE)
    ls_output = ls.stdout.decode("utf-8")
    assert "Europe/Prague" in ls_output


class TestWebServer(unittest.TestCase):
    name = "timezone"
    pipeline = "timezone.json"
    output_image = "timezone.tar.xz"

    @classmethod
    def setUpClass(cls) -> None:
        run_osbuild(rel_path(f"pipelines/{cls.pipeline}"))

    def test_timezone(self):
        with extract_image(self.output_image) as extract_dir:
            ls = subprocess.run(["ls", "-l", "etc/localtime"], cwd=extract_dir, check=True, stdout=subprocess.PIPE)
            ls_output = ls.stdout.decode("utf-8")
            assert "Europe/Prague" in ls_output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run integration tests')
    parser.add_argument('--list', dest='list', action='store_true', help='list test cases')
    parser.add_argument('--case', dest='specific_case', metavar='TEST_CASE', help='run single test case')
    args = parser.parse_args()

    logging.info(f"Using {OBJECTS} for objects storage.")
    logging.info(f"Using {OUTPUT_DIR} for output images storage.")
    logging.info(f"Using {OSBUILD} for building images.")

    web_server = IntegrationTestCase(
        name="web-server",
        pipeline="web-server.json",
        output_image="web-server.qcow2",
        test_cases=[test_web_server_with_curl],
        type=IntegrationTestType.BOOT_WITH_QEMU
    )
    timezone = IntegrationTestCase(
        name="timezone",
        pipeline="timezone.json",
        output_image="timezone.tar.xz",
        test_cases=[test_timezone],
        type=IntegrationTestType.EXTRACT
    )

    cases = [web_server, timezone]

    if args.list:
        print("Available test cases:")
        for case in cases:
            print(f" - {case.name}")
    else:
        if not args.specific_case:
            for case in cases:
                case.run()
        else:
            for case in cases:
                if case.name == args.specific_case:
                    case.run()
