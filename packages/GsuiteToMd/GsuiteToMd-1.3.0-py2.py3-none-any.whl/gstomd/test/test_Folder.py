# -*- coding: utf-8 -*-
import unittest
import logging


from gstomd.convert import GsuiteToMd

logger = logging.getLogger(__name__)


class FolderTest(unittest.TestCase):
    """Tests operations of corpus class.
    """

    def test_01(self):
        logger.debug("Begin")
        gstomd = GsuiteToMd(
            dest_folder="result_test1", pydrive_settings="configs/pydrive_settings.yaml"
        )
        logger.debug("gsuiteTomd  Created")
        gstomd.Folder(
            folder_id="1pdYxLHNCP1hqUZwwUkY8c_zUg-LXLWyx",)

        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
