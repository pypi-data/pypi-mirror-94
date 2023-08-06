import os

from configparser import NoSectionError, ConfigParser as SCP

from lib_utils import helper_funcs

class Config:
    """Config wrapper for storing and retrieving passwords and other info"""

    def __init__(self, package="custom_config"):
        """Creates config if not exists"""

        self.path = f"/etc/{package}.conf"
        if not os.path.exists(self.path):
            try:
                with open(self.path, "w+") as f:
                    pass
            except PermissionError as e:
                helper_funcs.run_cmds([f"sudo touch {self.path}",
                                       f"sudo chmod -R 777 {self.path}"])
    def write_section(self, section: str, kwargs: dict):
        """Writes section in config"""

        _config = SCP()
        _config.read(self.path)
        _config[section] = kwargs
        with open(self.path, "a") as f:
            _config.write(f)

    def read(self, section: str, tag: str, raw: bool = True):
        """Reads section, allows user to write if not exists"""

        try:
            _conf = SCP()
            _conf.read(self.path)
            return _conf.get(section, tag, raw=raw)
        except (NoSectionError, AttributeError) as e:
            input(f"Fill in desired section in {self.path}, then press enter")
            return self.read(section, tag)

    def get_creds(self, section: str, tags: list):
        """Returns credentials for a given section"""

        return [self.read(section, tag) for tag in tags]

##############################################
### Random Credentials specific to my apps ###
##############################################

    def blackboard_creds(self):
        """Returns netid and password"""

        return self.get_creds("Blackboard", ["netid", "password"])

    def discord_creds(self):
        """Returns email and password"""

        return self.get_creds("Discord", ["email", "password"])

    def webull_creds(self):
        return self.get_creds("Webull", ["email", "trade_token", "password", "security_q"])

    def webull_email_creds(self):
        return self.get_creds("Email", ["email", "password"])

    def ice_man_creds(self):
        return self.get_creds("Ice", ["email", "password"])
