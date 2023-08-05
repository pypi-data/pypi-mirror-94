import os
import sys
import io
import unittest
import pathlib
from mock import patch

from iotprovision.winc.pywinc import main

TEST_DATA_FOLDER = pathlib.Path(__file__).parent.absolute() / "data"
TEST_TMP_FOLDER = pathlib.Path(__file__).parent.absolute() / "tmp"

# Reference root certs storage file built by pywinc based on certs in FW version 19.5.4 (RSA keys)
WINC_REF_ROOT_CERTS_BIN = TEST_DATA_FOLDER / "winc_ref_bin/winc_build_ref_root_certs.bin"
# Reference root certs that are present in WINC FW 19.5.4 (RSA keys)
WINC_REF_ROOT_CERTS_FOLDER = TEST_DATA_FOLDER / "winc_ref_root_certs"
# Reference root certs storage file built by pywinc based on certs with ECC key
WINC_REF_ROOT_CERTS_ECC_BIN = TEST_DATA_FOLDER / "winc_ref_bin/winc_build_ref_root_certs_ecc.bin"
# Reference root certs that were used to build WINC_REF_ROOT_CERTS_ECC_BIN
WINC_REF_ROOT_CERTS_ECC_FOLDER = TEST_DATA_FOLDER / "winc_ref_root_certs_ecc"

# Reference client certs storage file built by pywinc
WINC_REF_CLIENT_CERTS_BIN = TEST_DATA_FOLDER / "winc_ref_bin/winc_build_ref_client_certs.bin"
# Reference client certs
WINC_REF_CLIENT_CERTS_FOLDER = TEST_DATA_FOLDER / "winc_ref_client_certs"

# Temporary file storage
TMP_FILE_BIN = TEST_TMP_FOLDER / "tmp.bin"

class TestWincCli(unittest.TestCase):
    def setUp(self):
        pathlib.Path(TEST_TMP_FOLDER).mkdir(parents=True, exist_ok=True)

    def _mock_stdout(self):
        """
        Returns stdout mock.

        Content sent to stdout can be fetched with mock_stdout.getvalue()
        """
        mock_stdout_patch = patch('sys.stdout', new_callable=io.StringIO)
        self.addCleanup(mock_stdout_patch.stop)
        return mock_stdout_patch.start()

    def _mock_stderr(self):
        """
        Returns stderr mock.

        Content sent to stderr can be fetched with mock_stderr.getvalue()
        """
        mock_stderr_patch = patch('sys.stderr', new_callable=io.StringIO)
        self.addCleanup(mock_stderr_patch.stop)
        return mock_stderr_patch.start()

    def test_decode_root_certs(self):
        """Test the decoding of a root certs storage object
        """
        mock_stdout = self._mock_stdout() # suppress output
        testargs = ["pywinc", "decode", "-m", "root-certs", "-i", "{}".format(WINC_REF_ROOT_CERTS_BIN)]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        self.assertTrue('Found 12 certificates in certificate storage' in mock_stdout.getvalue())
        self.assertTrue("Issuer name SHA1: b'f53fa20d03923086e7058a404bfbb07118e59e4d'" in mock_stdout.getvalue())
        self.assertTrue("Issuer name SHA1: b'b80d5ed351523fed853720a0acc0dc1377be160c'" in mock_stdout.getvalue())

    def test_decode_client_certs(self):
        """Test the decoding of a client certs storage object
        """
        mock_stdout = self._mock_stdout() # suppress output
        testargs = ["pywinc", "decode", "-m", "client-certs", "-i", "{}".format(WINC_REF_CLIENT_CERTS_BIN)]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        self.assertTrue('Files in client certificate storage: 3' in mock_stdout.getvalue())
        self.assertTrue('File name: CERT_4246303A7EDD58D40A64215AF4CE6470' in mock_stdout.getvalue())
        self.assertTrue('File name: CERT_4D2AEDAA0845252D57B600C062983EEC' in mock_stdout.getvalue())
        self.assertTrue('File name: ECDSA.lst' in mock_stdout.getvalue())
        
    def test_build_client_certs(self):
        """Test the building of a client cert storage object.
        """
        mock_stdout = self._mock_stdout() # suppress output
        testargs = ["pywinc", "build", "-m", "client-certs", "-i", "{}".format(WINC_REF_CLIENT_CERTS_FOLDER), "-o", "{}".format(TMP_FILE_BIN)]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        with open(WINC_REF_CLIENT_CERTS_BIN, "rb") as ref:
            with open(TMP_FILE_BIN, "rb") as build:
                self.assertEqual(ref.read(), build.read())
        
    def test_build_winc_ref_root_certs(self):
        """Test the building of the root certificate store.

        We use the certificates that were originally used for WINC FW as input (WINC_REF_ROOT_CERTS_FOLDER)
        and compare the built storage object (TMP_FILE_BIN) with a reference (WINC_REF_ROOT_CERTS_BIN).
        The reference storage object was built by pywinc and verified by comparing this to the original
        store in the WINC as well as testing the functionality. However, the original WINC storage object
        differs a bit to the one that we build and the reference because the original tool does not initialize the
        storage memory object properly which leads to some unprogrammed bytes being set. In other words,
        pywinc is not bug compatible with the original tool.
        """
        mock_stdout = self._mock_stdout() # suppress output
        testargs = ["pywinc", "build", "-m", "root-certs", "-i", "{}".format(WINC_REF_ROOT_CERTS_FOLDER), "-o", "{}".format(TMP_FILE_BIN)]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        with open(WINC_REF_ROOT_CERTS_BIN, "rb") as ref:
            with open(TMP_FILE_BIN, "rb") as build:
                self.assertEqual(ref.read(), build.read())

    def test_build_root_certs_ecc(self):
        """Test the building of the root certificate store with ECC based certificates

        Build root cert store from certificates located in WINC_REF_ROOT_CERTS_ECC_FOLDER.
        Store this in TMP_FILE_BIN.
        Compare TMP_FILE_BIN with reference WINC_REF_ROOT_CERTS_ECC_BIN.
        """
        mock_stdout = self._mock_stdout() # ignore output by re-routing
        testargs = ["pywinc", "build", "-m", "root-certs", "-i", "{}".format(WINC_REF_ROOT_CERTS_ECC_FOLDER), "-o", "{}".format(TMP_FILE_BIN)]
        with patch.object(sys, 'argv', testargs):
            retval = main()
        self.assertEqual(retval, 0)
        with open(WINC_REF_ROOT_CERTS_ECC_BIN, "rb") as ref:
            with open(TMP_FILE_BIN, "rb") as build:
                self.assertEqual(ref.read(), build.read())

    def test_get_help(self):
        """Test help output
        Check that help returns no error code and that it contains 'usage: pywinc' string.
        """
        mock_stdout = self._mock_stdout()
        testargs = ["pywinc", "--help"]
        with patch.object(sys, 'argv', testargs):
            # The --help argument is a built-in part of argparse so it will result in a SystemExit exception instead of
            #  a normal return code
            with self.assertRaises(SystemExit) as system_exit:
                main()
        self.assertEqual(system_exit.exception.code, 0)
        self.assertTrue('usage: pywinc' in mock_stdout.getvalue())


