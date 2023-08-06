from lib_utils import utils
import pytest

from .test_config import Test_Config
from ..config import Config


@pytest.fixture(autouse=True)
def config():
    """Initializes a config file. Gets the path. Deletes and reinits"""

    config = Config(package=Test_Config.test_config_package)
    utils.run_cmds(f"sudo rm {config.path}")
    config = Config(package=Test_Config.test_config_package)
    yield config
    utils.run_cmds(f"sudo rm {config.path}")
