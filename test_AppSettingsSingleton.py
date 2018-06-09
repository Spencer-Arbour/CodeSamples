import json
import logging
import os
from os.path import join, normpath
import pytest

from AppsettingsSingleton import AppSettingsSingleton
from FileLoader import LoadFileContent


@pytest.fixture(autouse=True, scope="function")
def setup(request):
    logging.disable(logging.CRITICAL)

    def finalize():
        AppSettingsSingleton.delete_instance_for_tests()

    request.addfinalizer(finalize)


class TestAppSettings(object):

    source_directory = "SourceDirectory"
    failure_folder = "FailureFolder"
    video_extensions = "VideoFileExtensions"
    delete_processed = "DeletedProcessed"
    retry_limit = "RetryLimit"
    retry_wait_ms = "RetryWaitMs"
    log_level = "LogLevel"

    default_source_directory = normpath(join(__file__, "..", "..", ".."))
    default_failure_folder = normpath(join(__file__, "..", "..", "..", "./failure"))
    default_video_extensions = ["avi", "wmv", "mp4", "mkv"]
    default_delete_processed = False
    default_retry_limit = 5
    default_retry_wait_ms = 60000
    default_log_level = "INFO"

    wrong_type = dict(
        SourceDirectory=34,
        FailureFolder=["haha", "lol"],
        VideoFileExtensions=True,
        DeletedProcessed="True",
        RetryLimit=False,
        RetryWaitMs="False",
        LogLevel=3423
    )

    correct_config = dict(
        SourceDirectory="/etc/home",
        FailureFolder="/lame_duck",
        VideoFileExtensions=["xlsx", "csv", "tar"],
        DeletedProcessed=True,
        RetryLimit=10,
        RetryWaitMs=100,
        LogLevel="WARN"
    )

    relative = dict(
        SourceDirectory="./etc/home",
        FailureFolder="./lame_ducks",
    )

    absolute = dict(
        SourceDirectory="/etc/home",
        FailureFolder="/lame_ducks",
    )

    under_min = dict(
        RetryLimit=-1,
        RetryWaitMs=-1
    )

    above_max = dict(
        RetryLimit=101,
        RetryWaitMs=600001
    )

    levels = dict(
        trace="TRACE",
        debug="DEBUG",
        info="INFO",
        warn="WARN",
        error="ERROR"
    )

    def test_permissions_error_on_config(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: exec('raise(PermissionError(x))'))

        with pytest.raises(PermissionError):
            AppSettingsSingleton("Locked_File")

    def test_invalid_json_in_config_file(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json",
                            lambda x: exec('raise(json.decoder.JSONDecodeError("invalid", x, 1))'))

        with pytest.raises(json.decoder.JSONDecodeError):
            AppSettingsSingleton("invalid_json_file")

    def test_config_file_not_found(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: exec('raise(FileNotFoundError(x))'))

        with pytest.raises(FileNotFoundError):
            AppSettingsSingleton("missing_file")

    def test_user_defaults_if_value_not_in_config(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: {})

        app = AppSettingsSingleton("value_not_in_config")
        self._assert_defaults(app)

    def test_use_defaults_if_config_type_are_incorrect(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: self.wrong_type)

        app = AppSettingsSingleton("incorrect_type_config")
        self._assert_defaults(app)

    def test_use_config_values(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: self.correct_config)

        app = AppSettingsSingleton("correct_config")

        assert self.correct_config[self.source_directory] == app.source_directory
        assert self.correct_config[self.failure_folder] == app.failure_folder
        assert self.correct_config[self.video_extensions] == app.video_extension
        assert self.correct_config[self.delete_processed] == app.delete_processed
        assert self.correct_config[self.retry_limit] == app.retry_limit
        assert self.correct_config[self.retry_wait_ms] == app.retry_wait_ms
        assert self.correct_config[self.log_level] == app.log_level

    def test_use_relative_paths_from_config(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: self.relative)

        app = AppSettingsSingleton("relative_path_config")

        path_to_file = join(__file__, "..", "..", "..")
        assert normpath(join(path_to_file, self.relative[self.source_directory])) == app.source_directory
        assert normpath(join(path_to_file, self.relative[self.failure_folder])) == app.failure_folder

    def test_use_absolute_paths_from_config(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: self.absolute)

        app = AppSettingsSingleton("absolute_path_config")

        assert self.absolute[self.source_directory] == app.source_directory
        assert self.absolute[self.failure_folder] == app.failure_folder

    def test_use_default_if_values_under_min(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: self.under_min)

        app = AppSettingsSingleton("under_min")

        assert app.retry_limit == 0
        assert app.retry_wait_ms == 0

    def test_use_default_if_values_above_max(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: self.above_max)

        app = AppSettingsSingleton("above_max")

        assert app.retry_limit == 100
        assert app.retry_wait_ms == 600000

    def test_valid_log_levels(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        for key, level in self.levels.items():
            monkeypatch.setattr(LoadFileContent, "load_json", lambda x: {self.log_level: level})
            app = AppSettingsSingleton("levels")
            assert app.log_level == level
            AppSettingsSingleton.delete_instance_for_tests()

    def test_default_log_level_when_invalid_level(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: {self.log_level: "WAR"})

        app = AppSettingsSingleton("levels")
        assert app.log_level == self.default_log_level

    def test_class_is_singleton(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isfile', lambda x: True)
        monkeypatch.setattr(LoadFileContent, "load_json", lambda x: self.correct_config)

        app1 = AppSettingsSingleton("part1")
        app2 = AppSettingsSingleton("part2")

        assert app2 is app1

    def _assert_defaults(self, app):
        assert self.default_source_directory == app.source_directory
        assert self.default_failure_folder == app.failure_folder
        assert self.default_video_extensions == app.video_extension
        assert self.default_delete_processed == app.delete_processed
        assert self.default_retry_limit == app.retry_limit
        assert self.default_retry_wait_ms == app.retry_wait_ms
        assert self.default_log_level == app.log_level
