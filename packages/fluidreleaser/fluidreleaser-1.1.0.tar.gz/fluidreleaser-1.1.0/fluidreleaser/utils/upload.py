#
# Copyright (C) 2021 ProjectFluid
#
# SPDX-License-Identifier: Apache-2.0
#

from fluidreleaser import SFTP_SERVER_HOST, SFTP_SERVER_PORT, private_key_path, SFTP_MAIN_DIR
from fluidreleaser.utils.artifact import Artifact
import os
from pathlib import PurePosixPath
import paramiko

class Uploader:
	def __init__(self, username: str):
		self.username = username
		self.current_file_base = None

		if not private_key_path.is_file():
			raise FileNotFoundError(f"Private SSH key doesn't exists in {private_key_path}")

		self.server = f"{SFTP_SERVER_HOST}:{SFTP_SERVER_PORT}"
		self.transport = paramiko.Transport(self.server)
		try:
			self.transport.connect(username=self.username,
								   pkey=paramiko.RSAKey.from_private_key_file(private_key_path))
		except paramiko.ssh_exception.AuthenticationException as e:
			print("Please add your public SSH key to https://sourceforge.net/auth/shell_services")
			raise e
		self.sftp = paramiko.SFTPClient.from_transport(self.transport)

		self.sftp.chdir(str(SFTP_MAIN_DIR))

	def upload(self, artifact: Artifact):
		"""
		Upload an artifact.

		Returns True if the upload went fine, else a string containing an explanation of the error 
		"""
		self.current_file_base = artifact.path.name

		if not artifact.path.is_file():
			return "File doesn't exists"

		self.sftp_chdir(PurePosixPath(artifact.device_codename) / artifact.android_version / artifact.variant)

		self.sftp.put(artifact.path, self.current_file_base, callback=self._print_progress)
		print("\n")

		# Return to root dir
		self.sftp.chdir(str(SFTP_MAIN_DIR))

		self.current_file_base = None

	def sftp_chdir(self, remote_directory: PurePosixPath):
		if remote_directory == '/':
			self.sftp.chdir('/')
			return
		if remote_directory == '':
			return
		try:
			self.sftp.chdir(str(remote_directory))
		except IOError:
			dirname, basename = os.path.split(str(remote_directory).rstrip('/'))
			self.sftp_chdir(dirname)
			self.sftp.mkdir(basename)
			self.sftp.chdir(basename)
			return True

	def _print_progress(self, transferred, toBeTransferred):
		percentage = format(transferred * 100 / toBeTransferred, '.2f')
		print(f"\r{self.current_file_base}: Transferred: {transferred} out of: {toBeTransferred} "
			  f"({percentage}%)", end="")

	def close(self):
		self.sftp.close()
		self.transport.close()
