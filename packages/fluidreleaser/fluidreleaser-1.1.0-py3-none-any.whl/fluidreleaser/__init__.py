#
# Copyright (C) 2021 ProjectFluid
#
# SPDX-License-Identifier: Apache-2.0
#

import os
from pathlib import Path, PurePosixPath

SFTP_SERVER_HOST = "frs.sourceforge.net"
SFTP_SERVER_PORT = 22
SFTP_MAIN_DIR = PurePosixPath("/") / "home" / "frs" / "project" / "project-fluid"
SF_BASE_URL = "https://sourceforge.net/projects/project-fluid/files"

OFFICIAL_DEVICES_REPO = "https://github.com/Project-Fluid-Devices/official_devices"

ANDROID_VERSIONS = {
	"Quenol": "ten",
	"Rum": "eleven"
}

NO_GAPPS = "gappless"
WITH_GAPPS = "gapped"
VARIANTS = [NO_GAPPS, WITH_GAPPS]
DEFAULT_VARIANT = NO_GAPPS

ALLOWED_BUILD_TYPES = ["OFFICIAL"]

module_path = Path(__file__)

current_path = Path(os.getcwd())
android_root = current_path
home_path = Path.home()

# SSH key
ssh_path = home_path / ".ssh"
private_key_path = ssh_path / "id_rsa"
