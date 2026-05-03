import os
import pwd
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)

class AppContext:
    def __init__(self, config: dict):
        self.config = config
        self.real_user = os.environ.get("SUDO_USER") or os.getlogin()
        pw = pwd.getpwnam(self.real_user)
        self.home_dir = Path(pw.pw_dir)
        
        self.config_dir: Path = home_dir / ".config" / "cli-core"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.chmod(0o740)
        
        self.cache_dir: Path = home_dir / ".cache" / "cli-core"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.chmod(0o740)
        
        logger.debug(
            f"AppContext initialized — user={self.real_user}"
        )
