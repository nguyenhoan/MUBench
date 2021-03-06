import logging
from os.path import join
from shutil import rmtree
from tempfile import mkdtemp
from unittest.mock import MagicMock, patch, PropertyMock

from nose.tools import assert_equals

from data.detector_execution import MineAndDetectExecution, Result
from data.findings_filters import FindingsFilter
from data.run import Run
from tests.data.stub_detector import StubDetector
from tests.test_utils.data_util import create_misuse, create_version, create_project
from utils.shell import Shell


class TestRun:
    # noinspection PyAttributeOutsideInit
    def setup(self):
        self.misuse = create_misuse('-misuse-', meta={"location": {"file": "a", "method": "m()"}})
        self.version = create_version("-version-", misuses=[self.misuse], project=create_project("-project-"))
        self.detector = StubDetector()

        self.temp_dir = mkdtemp(prefix='mubench-run-test_')
        self.findings_path = join(self.temp_dir, "-findings-")

        self.logger = logging.getLogger("test")

        self.__orig_shell_exec = Shell.exec
        Shell.exec = MagicMock()

    def teardown(self):
        rmtree(self.temp_dir)
        Shell.exec = self.__orig_shell_exec

    @patch("data.detector_execution.DetectorExecution.result", new_callable=PropertyMock)
    def test_not_run(self, result_mock):
        execution = MineAndDetectExecution(self.detector, self.version, self.findings_path, FindingsFilter())
        result_mock.return_value = None
        run = Run([execution])

        assert not run.is_success()
        assert not run.is_failure()

    @patch("data.detector_execution.DetectorExecution.result", new_callable=PropertyMock)
    def test_error(self, result_mock):
        execution = MineAndDetectExecution(self.detector, self.version, self.findings_path, FindingsFilter())
        result_mock.return_value = Result.error
        run = Run([execution])

        assert run.is_error()

    @patch("data.detector_execution.DetectorExecution.result", new_callable=PropertyMock)
    def test_timeout(self, result_mock):
        execution = MineAndDetectExecution(self.detector, self.version, self.findings_path, FindingsFilter())
        result_mock.return_value = Result.timeout
        run = Run([execution])

        assert run.is_timeout()

    @patch("data.detector_execution.DetectorExecution.result", new_callable=PropertyMock)
    def test_success(self, result_mock):
        execution = MineAndDetectExecution(self.detector, self.version, self.findings_path, FindingsFilter())
        result_mock.return_value = Result.success
        run = Run([execution])

        assert run.is_success()

    def test_get_potential_hits_ensures_unique_rank(self):
        execution1 = MagicMock()
        execution1.potential_hits = [{"rank": 0, "name": "finding1"}, {"rank": 1, "name": "finding2"}]
        execution2 = MagicMock()
        execution2.potential_hits = [{"rank": 0, "name": "finding3"}, {"rank": 1, "name": "finding4"}]
        run = Run([execution1, execution2])

        potential_hits = run.get_potential_hits()

        assert_equals(potential_hits, [
            {"rank": 0, "name": "finding1"},
            {"rank": 1, "name": "finding2"},
            {"rank": 2, "name": "finding3"},
            {"rank": 3, "name": "finding4"}])

    def test_get_potential_hits_preserves_rank(self):
        execution = MagicMock()
        execution.potential_hits = [{"rank": 42, "name": "f1"}, {"rank": 1337, "name": "f2"}]
        run = Run([execution])

        potential_hits = run.get_potential_hits()

        assert_equals(potential_hits, [
            {"rank": 42, "name": "f1"},
            {"rank": 1337, "name": "f2"}
        ])

    def test_get_number_of_findings(self):
        execution1 = MagicMock()
        execution1.number_of_findings = 5
        execution2 = MagicMock()
        execution2.number_of_findings = 42
        run = Run([execution1, execution2])

        number_of_findings = run.get_number_of_findings()

        assert_equals(number_of_findings, 5 + 42)

    def test_get_runtime(self):
        execution1 = MagicMock()
        execution1.runtime = 10
        execution2 = MagicMock()
        execution2.runtime = 5
        run = Run([execution1, execution2])

        runtime = run.get_runtime()

        assert_equals(runtime, 7.5)

