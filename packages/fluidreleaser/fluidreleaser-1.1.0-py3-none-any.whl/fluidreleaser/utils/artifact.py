#
# Copyright (C) 2021 ProjectFluid
#
# SPDX-License-Identifier: Apache-2.0
#

from fluidreleaser import ANDROID_VERSIONS, DEFAULT_VARIANT
import hashlib
from pathlib import Path

class Artifact:
	"""
	A class representing an artifact
	"""
	def __init__(self, artifact: Path):
		self.path = artifact
		self.filename = self.path.name
		filename_split = self.filename[:-4].split("-")
		if len(filename_split) == 6:
			filename_split.append(DEFAULT_VARIANT)

		(
			self.rom_name,
			self.version_number,
			self.version_name,
			self.build_type,
			self.device_codename,
			self.date,
			self.variant
		) = filename_split

		self.android_version = ANDROID_VERSIONS[self.version_name]

		self.sha1 = hashlib.sha1(self.path.read_bytes()).hexdigest()
