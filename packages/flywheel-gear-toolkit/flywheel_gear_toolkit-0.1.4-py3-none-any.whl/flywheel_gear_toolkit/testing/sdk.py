from unittest.mock import Mock

import flywheel
import pytest

# See https://github.com/pytest-dev/pytest-mock/  for mocker fixture


@pytest.fixture(scope="function")
def get_sdk_mock(mocker):
    spec = dir(flywheel.Flywheel)
    spec.extend(dir(flywheel.Client))
    spec.extend(["api_client", "deid_log"])
    sdk_mock = Mock(spec=spec)
    get_sdk_mock = mocker.patch("flywheel.Client", return_value=sdk_mock)
    return get_sdk_mock


@pytest.fixture(scope="function")
def sdk_mock(get_sdk_mock):
    return get_sdk_mock.return_value


@pytest.fixture(scope="function")
def job():
    default_id = "a-job-id"
    default_config = {
        "config": {"config0": "tomato"},
        "destination": {"id": "no-ex"},
        "inputs": {
            "file0": {
                "base": "file",
                "location": {"name": "a-filename"},
                "hierarchy": {"id": "an-id"},
            }
        },
    }
    default_gear_info = GEAR_0
    default_inputs = [
        {
            "id": "an-id",
            "input": "file0",
            "name": "a-filename",
            "type": "acquisition",
        }
    ]

    def get_job(id_=None, inputs=None, config=None, gear_info=None):
        if id_ is None:
            id_ = default_id
        if config is None:
            config = default_config
        if inputs is None:
            inputs = default_inputs
        if gear_info is None:
            gear_info = default_gear_info
        return flywheel.Job(
            id=id_,
            inputs=inputs,
            config=config,
            gear_info=gear_info,
        )

    return get_job
