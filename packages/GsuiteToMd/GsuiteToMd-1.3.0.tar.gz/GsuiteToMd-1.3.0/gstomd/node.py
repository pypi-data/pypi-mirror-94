# -*- coding: utf-8 -*-

import logging
from gstomd.utils import slugify

logger = logging.getLogger(__name__)


class Node:
    """
    class for Google Drive item
    """

    def __init__(self, googleDriveFile, path="", depth=1, drive_connector=""):
        """Create an instance of Node (class parent of GFolder and GDoc)

        Args:
            googleDriveFile (GoogleDriveFile, optional): returned by drive api.
            path (str, optional): Path (on disk) to the node.
            depth (int, optional): Depth of the node in the tree (from root).
            drive_connector (GoogleDrive, optional): created  by convert.GsuiteToMd.

        """
        self._googleDriveFile = googleDriveFile
        self.drive_connector = drive_connector
        self.path = path
        self.depth = depth
        self.is_fetched = False

    def unix_name(self):
        """Generate Unix name (no special caracters) from Node name.
        """
        return slugify(self.basename())

    def parent(self):
        """pass accesses to googleDriveFile
        """
        if self._googleDriveFile and self._googleDriveFile["parents"]:
            return self._googleDriveFile["parents"][0]["id"]
        return ""

    def id(self):
        """pass accesses to googleDriveFile
        """
        if self._googleDriveFile:
            return self._googleDriveFile["id"]
        return ""

    def basename(self):
        """pass accesses to googleDriveFile
        """
        if self._googleDriveFile:
            return self._googleDriveFile["title"]
        return ""
