# -*- coding: utf-8 -*-

import logging
import os
import shutil
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from gstomd.node import Node

logger = logging.getLogger(__name__)


class Gdoc(Node):

    """Google Document instance.
    Inherits Node.
    """

    def __str__(self):
        """Generate printable description
        """
        return "\n%sD : %20s|%30s|%20s|%s" % (
            "-" * self.depth * 4,
            self.basename(),
            self.id(),
            self.unix_name(),
            self.path,
        )

    def fetch(self):
        """Fetch document content from drive
        """
        logger.debug("fetch content for %s", self)
        self._googleDriveFile.FetchContent(
            mimetype="application/zip", remove_bom=True
        )
        self.is_fetched = True

    def to_disk(self):
        """Download document to disk as markdown + images in a subfolder
        """
        if not self.is_fetched:
            self.fetch()
        dirpath = Path(self.path)
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.makedirs(self.path)
        zip_path = self.path + "/" + os.path.basename(self.path) + ".zip"
        md_path = self.path + "/" + os.path.basename(self.path) + ".md"
        f_zip = open(zip_path, "wb")
        f_zip.write(self._googleDriveFile.content.getvalue())
        f_zip.close()
        with zipfile.ZipFile(zip_path, "r") as zip_ref:

            files_names = zip_ref.namelist()
            for file_name in files_names:
                if file_name.endswith(".html"):
                    f_md = open(md_path, "w")
                    html = zip_ref.read(file_name)
                    parsed_html = BeautifulSoup(html, features="lxml")
                    body = "%s" % (parsed_html.body)

                    body_md = md(body)
                    meta_id = "gsuiteid: " + self.id()
                    f_md.write(body_md)
                    f_md.close()
                    f_md = open(md_path, "r")
                    contents = f_md.readlines()
                    f_md.close()
                    contents.insert(1, meta_id)

                    f_md = open(md_path, "w")
                    contents = "".join(contents)
                    f_md.write(contents)
                    f_md.close()

                else:
                    zip_ref.extract(file_name, os.path.dirname(md_path))
            os.remove(zip_path)
