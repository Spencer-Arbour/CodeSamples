import json
import os
from typing import List

from FileLoader import LoadFileContent


class AppSettingsSingleton:

    _SINGLE_INSTANCE = None

    class _AppSettings:
        _SOURCE_DIRECTORY_DEFAULT = "."

        _FAILURE_FOLDER_DEFAULT = "./failure"

        _VIDEO_EXTENSIONS_DEFAULT = ["avi", "wmv", "mp4", "mkv"]

        _DELETE_PROCESSED_DEFAULT = False

        _RETRY_LIMIT_DEFAULT = 5
        _RETRY_LIMIT_MIN = 0
        _RETRY_LIMIT_MAX = 100

        _RETRY_WAIT_MS_DEFAULT = 60000
        _RETRY_WAIT_MS_MIN = 0
        _RETRY_WAIT_MS_MAX = 600000

        _LOG_LEVEL_DEFAULT = "INFO"
        _LOG_LEVEL_VALID_LEVELS = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR"]

        @property
        def source_directory(self):
            return self._source_directory

        @property
        def failure_folder(self):
            return self._failure_folder

        @property
        def video_extension(self):
            return self._video_extensions

        @property
        def delete_processed(self):
            return self._delete_processed

        @property
        def retry_limit(self):
            return self._retry_limit

        @property
        def retry_wait_ms(self):
            return self._retry_wait_ms

        @property
        def log_level(self):
            return self._log_level

        def __init__(self, config: str) -> None:
            self._config = config
            self._config_content = None
            self._app_settings = None

            self._source_directory = None
            self._failure_folder = None
            self._video_extensions = None
            self._delete_processed = None
            self._retry_limit = None
            self._retry_wait_ms = None
            self._log_level = None

        def _read_appsettings_file(self) -> "_AppSettings":
            if os.path.isfile(self._config):
                try:
                    self._config_content = LoadFileContent.load_json(self._config)
                except PermissionError as e:
                    raise PermissionError(
                        "The program could not access it's config file at '{0}' due to permissions "
                        "issue. Please resolve the problem and attempt to run the program again."
                        .format(self._config)
                    ).with_traceback(e.__traceback__)
                except json.decoder.JSONDecodeError as e:
                    raise json.decoder.JSONDecodeError(
                        "The program config file at '{0}' could not be parsed due to a json decoding error. Please fix "
                        "resolve the problem and attempt to run the program again.".format(self._config), e.doc, e.pos
                    ).with_traceback(e.__traceback__)
            else:
                raise FileNotFoundError (
                    "The program config file could not be found at '{0}'. Please resolve the "
                    "problem and attempt to run the program again.".format(self._config)
                )
            return self

        def _set_values(self) -> "_AppSettings":
            self._source_directory = self._get_directory(
                self._config_content.get("SourceDirectory", None),
                self._SOURCE_DIRECTORY_DEFAULT
            )

            self._failure_folder = self._get_directory(
                self._config_content.get("FailureFolder", None),
                self._FAILURE_FOLDER_DEFAULT
            )

            self._video_extensions = self._get_value(
                self._config_content.get("VideoFileExtensions", None),
                self._VIDEO_EXTENSIONS_DEFAULT
            )

            self._delete_processed = self._get_value(
                self._config_content.get("DeletedProcessed", None),
                self._DELETE_PROCESSED_DEFAULT
            )

            self._retry_limit = self._get_int(
                self._config_content.get("RetryLimit", None),
                self._RETRY_LIMIT_DEFAULT,
                self._RETRY_LIMIT_MIN,
                self._RETRY_LIMIT_MAX
            )

            self._retry_wait_ms = self._get_int(
                self._config_content.get("RetryWaitMs", None),
                self._RETRY_WAIT_MS_DEFAULT,
                self._RETRY_WAIT_MS_MIN,
                self._RETRY_WAIT_MS_MAX
            )

            self._log_level = self._get_level(
                self._config_content.get("LogLevel"),
                self._LOG_LEVEL_DEFAULT,
                self._LOG_LEVEL_VALID_LEVELS
            )

            return self

        def _get_directory(self, value_from_config: str, default_value: str) -> str:
            if self._is_both_matching_types(value_from_config, default_value):
                if os.path.isabs(value_from_config):
                    return value_from_config
                else:
                    return os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", value_from_config))
            else:
                return os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", default_value))

        def _get_int(self, value_from_config: int, default_value: int, minimum: int, maximum: int) -> int:
            if self._is_both_matching_types(value_from_config, default_value):
                return sorted([minimum, value_from_config, maximum])[1]
            else:
                return default_value

        def _get_value(self, value_from_config, default_value):
            if self._is_both_matching_types(value_from_config, default_value):
                return value_from_config
            else:
                return default_value

        def _get_level(self, value_from_config: str, default_value: str, valids: List[str]):
            if self._is_both_matching_types(value_from_config, default_value):
                if value_from_config in valids:
                    return value_from_config
            return default_value

        @staticmethod
        def _is_both_matching_types(value_from_config, default_value):
            if type(default_value) is list and type(value_from_config) is list:
                return all(isinstance(value, type(default_value[0])) for value in value_from_config)
            else:
                return type(value_from_config) == type(default_value)

        def __str__(self):
            configs = self._config_values_header()

            for key, value in self._app_settings.items():
                configs.append("{0}: '{1}'".format(key, value))

            return "\n".join(configs)

        @staticmethod
        def _config_values_header() -> List[str]:
            return [
                "------------------------------",
                "ConfigValues",
                "------------------------------"
            ]

    def __new__(cls, config: str=None):
        if not cls._SINGLE_INSTANCE:

            cls._SINGLE_INSTANCE = (
                cls._AppSettings(config)
                    ._read_appsettings_file()
                    ._set_values()
            )

        return cls._SINGLE_INSTANCE

    @classmethod
    def delete_instance_for_tests(cls):
        cls._SINGLE_INSTANCE = None
