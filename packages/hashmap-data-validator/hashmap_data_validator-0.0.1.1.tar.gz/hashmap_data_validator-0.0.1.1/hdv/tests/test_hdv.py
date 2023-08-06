from hdv import Validator
import os
from hdv.utils.parse_config import ParseConfig
from hdv.utils.project_config import ProjectConfig

if __name__ == "__main__":
    os.environ['HDV_ENV'] = "dev"
    config = ParseConfig.parse(config_path=f"{ProjectConfig.hdv_home()}/{ProjectConfig.configuration_path()}")
    Validator(configuration=config).run()
