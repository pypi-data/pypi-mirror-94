# -*- coding: utf-8 -*-
import logging


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from gstomd.gfolder import Gfolder
from gstomd.gdoc import Gdoc


logger = logging.getLogger(__name__)


DEFAULT_SETTINGS = {
    "pydrive_settings": "pydrive_settings.yaml",
    "dest_folder": "gstomd_extract",
}


class GsuiteToMd:
    def __init__(
        self,
        pydrive_settings=DEFAULT_SETTINGS["pydrive_settings"],
        dest_folder=DEFAULT_SETTINGS["dest_folder"],
    ):
        """Create an instance of GsuiteToMd.

        """

        self.dest_folder = dest_folder
        self.pydrive_settings = pydrive_settings
        logger.info(
            "Settings : dest_folder %s, pydrive_settings %s",
            self.dest_folder,
            self.pydrive_settings,
        )
        self.ga = GoogleAuth(self.pydrive_settings)
        self.drive_connector = GoogleDrive(self.ga)

    def Folder(self, folder_id,):
        f = Gfolder(
            googleDriveFile="",
            path="",
            depth=1,
            drive_connector=self.drive_connector,
            root_folder_id=folder_id,
            dest_folder=self.dest_folder,
        )

        f.fetch()
        f.to_disk()

    def Gdoc(self, doc_id, dest_folder):
        doc = Gdoc(self.drive_connector, doc_id, dest_folder)
        doc.fetch()
        doc.to_disk()
