from cli_core.app import Config

def make_config() -> Config:
    # It populates the standard AppConfig dataclass structure that cli_core provides.
    config = Config()
    config.custom1 = {}
    config.custom2 = {}
    return config

operations = Operations()
