# -*- coding: utf-8 -*-

import logging
import os
import shutil
from pathlib import Path

from gstomd.gdoc import Gdoc
from gstomd.node import Node
from gstomd.utils import mime_to_filetype

logger = logging.getLogger(__name__)


class Gfolder(Node):

    """Folder instance.
    Inherits Node.
    """

    def __init__(
        self,
        googleDriveFile="",
        path="",
        depth=1,
        drive_connector="",
        dest_folder="",
        root_folder_id="",
    ):
        """Create an instance of Gdolder

        Args:
            googleDriveFile (GoogleDriveFile, optional): see Node.
            path (str, optional): see Node.
            depth (int, optional): see Node.
            drive_connector (str, optional): instance of GoogleDrive.
            dest_folder (str, optional): The destination folder on disk.
            root_folder_id (str, optional): id of the root folder in Gdrive.
        """
        super().__init__(
            googleDriveFile=googleDriveFile,
            path=path,
            depth=depth,
            drive_connector=drive_connector,
        )
        self.children = []
        self.dest_folder = dest_folder
        self.root_folder_name = ""
        self.root_folder_id = root_folder_id
        logger.debug(self)

    def __str__(self):
        """Generate printable description
        """
        message = "\n%sF : %20s|%30s|%20s|%s" % (
            "-" * self.depth * 4,
            self.basename(),
            self.id(),
            self.unix_name(),
            self.path,
        )
        for child in self.children:
            message = "%s%s" % (message, child)
        return message

    def fetch(self):
        """
        Generate folder structure with files
        """

        nodes = {}
        query = (
            "trashed=false and mimeType='application/vnd.google-apps.folder'"
        )
        file_list = self.drive_connector.ListFile({"q": query}).GetList()

        file_list = self.drive_connector.ListFile(
            {
                "q": query,
                "corpora": "allDrives",
                "includeItemsFromAllDrives": True,
                "supportsAllDrives": True,
            },
        ).GetList()
        logger.debug("%d folders found", sum(1 for x in file_list))

        for item in file_list:
            if item["id"] == self.root_folder_id:

                self._googleDriveFile = item
                folder = self

                self.root_folder_name = self.unix_name()

                self.path = "%s/%s" % (self.dest_folder, self.unix_name(),)

            else:
                folder = Gfolder(item)
            nodes[folder.id()] = (folder, folder.parent())

        for folder_id, (folder, parent_id) in nodes.items():

            if parent_id is None:
                continue
            if parent_id in nodes.keys():
                nodes[parent_id][0].children.append(folder)
            else:
                logger.debug("parent id %s not found ", parent_id)

        self.complement_children_path_depth()
        folders = self.all_subfolders()
        parents_id = " or ".join(
            "'{!s}' in parents".format(key) for key in folders
        )

        query_for_files = (
            "trashed=false and mimeType='application/vnd.google-apps.document' and ("
            + parents_id
            + ")"
        )

        logger.debug("Query for files : %s", query_for_files)
        file_list = self.drive_connector.ListFile(
            {
                "q": query_for_files,
                "corpora": "allDrives",
                "includeItemsFromAllDrives": True,
                "supportsAllDrives": True,
            },
        ).GetList()
        logger.debug("%d files found", sum(1 for x in file_list))

        for item in file_list:
            if mime_to_filetype(item["mimeType"]) != "DOC":
                logger.debug("%s %s", item["title"], item["mimeType"])
                continue
            doc = Gdoc(item)
            logger.debug("Doc found %s", doc)

            if doc.parent() in nodes.keys():
                nodes[doc.parent()][0].children.append(doc)
                logger.debug(
                    "doc added as children of %s", nodes[doc.parent()][0]
                )
            else:
                logger.debug("parent id %s not found", doc.parent())
        self.complement_children_path_depth()

        logger.debug(self)
        self.fetched = True
        return self

    def to_disk(self):
        """Create folder and all his subfolders and google documents on the disk
        """
        dirpath = Path(self.path)
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.makedirs(self.path)
        if self.children:
            for child in self.children:
                if isinstance(child, Gfolder):
                    child.to_disk()

                elif isinstance(child, Gdoc):
                    child.to_disk()

    def all_subfolders(self):
        """
        list all subfolders under self
        """
        list_folders = set()

        for child in self.children:
            if isinstance(child, Gfolder):
                list_folders.add(child.id())
                child_folders = child.all_subfolders()
                if child_folders:
                    list_folders = list_folders.union(child_folders)
        return list_folders

    def complement_children_path_depth(self):
        """
        generate children's path and depth information from basename
        """
        for child in self.children:
            child.path = "{0}/{1}".format(self.path, child.unix_name())
            child.depth = self.depth + 1
            if isinstance(child, Gfolder):
                child.complement_children_path_depth()
