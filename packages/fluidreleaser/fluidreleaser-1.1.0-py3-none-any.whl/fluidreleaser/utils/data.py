#
# Copyright (C) 2021 ProjectFluid
#
# SPDX-License-Identifier: Apache-2.0
#

from fluidreleaser import OFFICIAL_DEVICES_REPO, SF_BASE_URL
from fluidreleaser.utils.artifact import Artifact
import datetime
from git import Repo
import json
from pathlib import Path
from shutil import rmtree
from stat import S_IWRITE
from tempfile import TemporaryDirectory

def handle_remove_readonly(func, path, _):
	Path(path).chmod(S_IWRITE)
	func(path)

class OTAData:
	def __init__(self):
		self.tempdir = TemporaryDirectory()
		self.path = Path(self.tempdir.name)
		if self.path.is_dir():
			rmtree(self.path, ignore_errors=False, onerror=handle_remove_readonly)

		self.repo = Repo.clone_from(OFFICIAL_DEVICES_REPO, self.path)

	def update(self, artifact: Artifact):
		flavor = f"{artifact.android_version}_{artifact.variant}"
		ota_dict = {
			"filename": artifact.filename,
			"flavor": flavor,
			"version": artifact.version_number,
			"url": f"{SF_BASE_URL}/{artifact.device_codename}/{artifact.android_version}/{artifact.variant}/{artifact.filename}/download",
			"size": str(artifact.path.stat().st_size),
			"datetime": int(datetime.datetime.now().timestamp()),
			"sha1sum": artifact.sha1
		}
		json.dump(ota_dict, (self.path / artifact.device_codename / f"{flavor}.json").open("w"),
				  indent=4)
		self.repo.index.add(["*"])
		self.repo.index.commit(f"[FluidCI] {artifact.device_codename}: {artifact.android_version}: {artifact.variant}: Update to {artifact.date}")

	def push_to_repo(self):
		remote_url = self.repo.remotes[0].config_reader.get("url")
		self.repo.git.push(remote_url, "master")
