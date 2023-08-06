#
# Copyright (C) 2021 ProjectFluid
#
# SPDX-License-Identifier: Apache-2.0
#

from fluidreleaser import ALLOWED_BUILD_TYPES, android_root
from fluidreleaser.utils.artifact import Artifact
from fluidreleaser.utils.data import OTAData
from fluidreleaser.utils.upload import Uploader
from argparse import ArgumentParser
from logging import basicConfig, DEBUG
from os import environ

def main():
	parser = ArgumentParser()
	parser.add_argument("-d", "--debug", action="store_true",
						help="enable debug/verbose mode")
	args = parser.parse_args()

	if args.debug:
		basicConfig(format='[%(asctime)s] [%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
					level=DEBUG)

	codename = environ.get('FLUID_BUILD', None)
	if codename is None:
		raise AssertionError("FLUID_BUILD not defined, "
							 "please lunch your device before executing this script")

	out_dir = android_root / "out" / "target" / "product" / codename
	artifacts = [Artifact(artifact) for artifact in list(out_dir.glob("Fluid-*.zip"))]
	artifacts = [artifact for artifact in artifacts if artifact.build_type in ALLOWED_BUILD_TYPES]

	if len(artifacts) == 0:
		raise FileNotFoundError("Error: No builds have been found")

	approved_artifacts = [artifact for artifact in artifacts
						  if input(f"Do you want to upload {artifact.filename}? [y/N]: ") in ['y', 'Y']]

	if len(approved_artifacts) == 0:
		exit()

	username = input("SourceForge username: ")
	uploader = Uploader(username)
	otadata = OTAData()

	for artifact in approved_artifacts:
		uploader.upload(artifact)
		otadata.update(artifact)

	otadata.push_to_repo()

	print("All done")
