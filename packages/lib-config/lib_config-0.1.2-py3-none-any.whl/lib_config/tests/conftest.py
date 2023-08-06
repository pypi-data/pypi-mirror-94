from lib_utils import helper_funcs
import pytest

from .test_config import Test_Config
from ..config import Config


@pytest.fixture(autouse=True)
def config():
    """Initializes a config file. Gets the path. Deletes and reinits"""

    config = Config(package=Test_Config.test_config_package)
    helper_funcs.run_cmds(f"sudo rm {config.path}")
    config = Config(package=Test_Config.test_config_package)
    yield config
    helper_funcs.run_cmds(f"sudo rm {config.path}")
