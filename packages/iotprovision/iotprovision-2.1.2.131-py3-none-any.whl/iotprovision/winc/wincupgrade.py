import logging
from .winc_flash_map import FlashMap

HDR_SIZE = 8
PAYLOAD_SIZE_PAGE = 1
PAYLOAD_SIZE_SECTOR = 16
PAGE_SIZE = 256

WINC_BRIDGE_SOF_TOKEN = 0xAA
WINC_BRIDGE_EOF_TOKEN = 0xBB

class WincUpgradeError(Exception):
    """
    WINC upgrade specific exception
    """

    def __init__(self, msg=None, code=0):
        super(WincUpgradeError, self).__init__(msg)
        self.code = code

class ProgressLogger():
    """Simple progress logger

    Logs progress using logging module.
    The ProgressLogger will log a message every step_percents until current_value reaches range
    Example:
        Progress logger for a function writing to a memory with 256 pages, logging a message for every 10%
        .. highlight:: python
        .. code-block:: python

            progresslogger = ProgressLogger(256, 10, "written")
            for page_index in range(256):
                writePage()
                progresslogger.log(page_index)
    """
    def __init__(self, logger, start, end, step_percents=10, msg=""):
        """
        :param logger: logger object, typically fetched using logging.getLogger()
        :type logger: :class:`logging.Logger` object
        :param start: start value
        :type start: int of float
        :param end: end value
        :type end: int or float
        :param step_percents: step size for logging, i.e. logging will only happen every step_percents, defaults to 10
        :type step_percents: int, optional
        :param msg: progress message to be appended after the percentage output, defaults to ""
        :type msg: str, optional
        """
        self.logger = logger
        self.start = start
        self.total_range = end - self.start
        self.step_percents = step_percents
        self.msg = msg
        # Setting currently logged progress to negative step to ensure logging also at 0 %
        self.logged_progress = -step_percents

    def log(self, absolute_progress):
        """Log current progress if passed the step size

        :param progress: current progress
        :type progress: int or float
        """
        progress = ((absolute_progress-self.start)*100) / self.total_range
        if (progress - self.logged_progress) > self.step_percents:
            self.logged_progress = int(progress)
            self.logger.info("%d%% %s", self.logged_progress, self.msg)

class WincUpgradeBridgeCmdRsp:
    """
    Command/response generator for WINC upgrade bridge
    """
    def __init__(self, serial):
        self.serial = serial
        self.logger = logging.getLogger(__name__)
        self.max_rsp_size = (PAYLOAD_SIZE_PAGE * PAGE_SIZE) + HDR_SIZE
        self.rsp_token_location = ((PAYLOAD_SIZE_PAGE * PAGE_SIZE) + HDR_SIZE)-1

    def _send_receive(self, cmd, rsp_size):
        """
        Send a command and wait for a response
        :param cmd: read request to send
        :param rep_size: number of bytes to expect in return
        :return: response received
        """
        self.serial.write(cmd)
        rsp_str = self.serial.read(rsp_size)
        if len(rsp_str) < rsp_size:
            msg = "Invalid response packet from WINC bridge"
            raise WincUpgradeError(msg)
        return bytearray(rsp_str)

    def send_receive_read(self, cmd, rsp_size):
        """
        Send a READ command and receive the response
        :param cmd: read request to send
        :return: response received
        """
        rsp = self._send_receive(cmd, rsp_size)
        if rsp[1] != 0:
            msg = "Error reading from WINC"
            raise WincUpgradeError(msg)

        if rsp[0] != WINC_BRIDGE_SOF_TOKEN or rsp[rsp_size-1] != WINC_BRIDGE_EOF_TOKEN:
            msg = "Invalid data returned from WINC"
            raise WincUpgradeError(msg)

        return rsp


    def send_receive_write(self, cmd):
        """
        Send a WRITE command and receive the response
        :param cmd: write request to send
        """
        rsp = self._send_receive(cmd, HDR_SIZE)
        if rsp[1] == 0:
            return
        msg = "Error writing to WINC"
        raise WincUpgradeError(msg)


class WincUpgradeBridgeLink:
    """
    Read / write link driver for Winc1500
    """
    READ_FW_VER = 0
    READ_PAGE = 1
    READ_SECTOR = 2
    WRITE_PAGE = 3
    WRITE_SECTOR = 4
    ERASE_SECTOR = 5
    WINC_RESET = 6

    def __init__(self, serial):
        self.winccmd = WincUpgradeBridgeCmdRsp(serial)
        self.logger = logging.getLogger(__name__)

    def read_command(self, command_id, offset):
        cmd = bytearray()
        cmd.append(WINC_BRIDGE_SOF_TOKEN)
        cmd.append(command_id)
        # No payload
        cmd.append(0)
        cmd.extend(offset.to_bytes(4, 'little'))
        #cmd.extend(([0x00]*(PAYLOAD_SIZE_0)))    # Dummy data
        cmd.append(WINC_BRIDGE_EOF_TOKEN)
        return cmd

    def write_command(self, command_id, payload_size, offset, data):
        cmd = bytearray()
        cmd.append(WINC_BRIDGE_SOF_TOKEN)
        cmd.append(command_id)
        cmd.append(payload_size)
        cmd.extend(offset.to_bytes(4, 'little'))
        cmd.extend(data)
        cmd.append(WINC_BRIDGE_EOF_TOKEN)
        return cmd

    def read_firmware_version(self):
        """
        """
        self.logger.debug("Reading WINC firmware version")
        cmd = self.read_command(self.READ_FW_VER, 0)
        rsp_size = PAYLOAD_SIZE_PAGE * PAGE_SIZE + HDR_SIZE
        rsp = self.winccmd.send_receive_read(cmd, rsp_size)
        return rsp[HDR_SIZE+3:HDR_SIZE+9]

    def reset(self):
        """
        """
        self.logger.debug("Reseting WINC")
        cmd = self.read_command(self.WINC_RESET, 0)
        self.winccmd.send_receive_write(cmd)

    def read_page(self, offset): #it would read 256 bytes
        """
        """
        self.logger.debug("Reading page from WINC")
        cmd = self.read_command(self.READ_PAGE, offset)
        rsp_size = PAYLOAD_SIZE_PAGE * PAGE_SIZE + HDR_SIZE
        rsp = self.winccmd.send_receive_read(cmd, rsp_size)
        return rsp[HDR_SIZE-1:rsp_size-1]

    def read_sector(self, offset): #it would read 4096 bytes
        """
        """
        self.logger.debug("Reading sector from WINC")
        cmd = self.read_command(self.READ_SECTOR, offset)
        rsp_size = PAYLOAD_SIZE_SECTOR * PAGE_SIZE + HDR_SIZE
        rsp = self.winccmd.send_receive_read(cmd, rsp_size)
        return rsp[HDR_SIZE-1:rsp_size-1]

    def write_page(self, offset, data):  # TODO: In order to write a page a sector erase is needed, should this be automated?
        """
        """
        self.logger.debug("Writing page to WINC")
        if len(data) != PAYLOAD_SIZE_PAGE * PAGE_SIZE:
            msg = "Invalid data length writing to WINC"
            raise WincUpgradeError(msg)

        cmd = self.write_command(self.WRITE_PAGE, PAYLOAD_SIZE_PAGE, offset, data)
        self.winccmd.send_receive_write(cmd)

    def write_sector(self, offset, data):  # TODO: In order to write a page a sector erase is needed, should this be automated?
        self.logger.debug("Writing sector to WINC")
        if len(data) != PAYLOAD_SIZE_SECTOR * PAGE_SIZE:
            msg = "Invalid data length writing to WINC"
            raise WincUpgradeError(msg)

        cmd = self.write_command(self.WRITE_SECTOR, PAYLOAD_SIZE_SECTOR, offset, data)
        self.winccmd.send_receive_write(cmd)

    def erase_sector(self, offset):
        """
        """
        self.logger.debug("Erasing sector on WINC")
        cmd = self.read_command(self.ERASE_SECTOR, offset)
        self.winccmd.send_receive_write(cmd)


class WincUpgrade:
    def __init__(self, serial, loglevel=logging.INFO):
        self.link = WincUpgradeBridgeLink(serial)
        self.logger = logging.getLogger(__name__)

    def check_bridge(self):
        try:
            self.logger.info("Checking WINC bridge connection.")
            version_info = self.link.read_firmware_version()
            return True
        except:
            self.logger.error("No reponse from WINC")
            return False

    def reset(self):
        self.logger.info("Reseting WINC connection")
        self.link.reset()

    def read_firmware_version(self):
        self.logger.info("Reading WINC FW version")
        version_info = self.link.read_firmware_version()
        fw_version = "{}.{}.{}".format(version_info[0], version_info[1], version_info[2])
        driver_version = "{}.{}.{}".format(version_info[3], version_info[4], version_info[5])
        self.logger.debug("- WINC firmware version: %s", fw_version)
        self.logger.debug("- WINC driver version required: %s", driver_version)
        return fw_version, driver_version

    def erase_sector(self, sector_offset):
        self.logger.debug("Erasing sector at 0x%x", sector_offset)
        self.link.erase_sector(sector_offset)

    def erase_flash(self):
        self.logger.info("Erasing WINC flash")
        flash_offset = FlashMap.start_addr
        erase_progress = ProgressLogger(self.logger, FlashMap.start_addr, FlashMap.total_flash_size, msg="erased")
        while flash_offset < (FlashMap.total_flash_size):
            erase_progress.log(flash_offset)
            self.erase_sector(flash_offset)
            flash_offset += FlashMap.sector_size

        self.logger.info("Flash Erase Done")

    def write_sector(self, sector_offset, data):
        self.logger.debug("Writing sector at 0x%x", sector_offset)
        self.link.write_sector(sector_offset, data)

    def write_flash(self, data):
        self.logger.info("Writing WINC flash")
        flash_offset = FlashMap.start_addr
        sector_num = 0
        remaining_bin_size = len(data)
        sector_size = PAYLOAD_SIZE_SECTOR*PAGE_SIZE
        sector_progress = ProgressLogger(self.logger, 0, remaining_bin_size/sector_size, msg="written")
        while remaining_bin_size > PAYLOAD_SIZE_SECTOR * PAGE_SIZE:
            self.logger.debug("Writing sector at 0x%x", flash_offset + sector_size*sector_num)
            sector_progress.log(sector_num)
            self.link.write_sector(flash_offset + sector_size*sector_num, data[sector_size*sector_num:sector_size*(sector_num+1)])
            sector_num += 1
            remaining_bin_size -= sector_size
        if remaining_bin_size:
            self.logger.debug("Writing final sector")
            rem_data = data[sector_size*sector_num::]
            while len(rem_data) < sector_size:
                rem_data += '\xFF'
            self.link.write_sector (flash_offset + sector_size*sector_num, rem_data)
        self.logger.info("Flash write complete")

    def read_sector(self, sector_offset):
        flash_data = bytearray()
        flash_data.extend(self.link.read_sector(sector_offset))
        return flash_data

    def read_flash(self):
        self.logger.info("Reading back WINC flash")
        flash_data = bytearray()
        flash_offset = FlashMap.start_addr
        total_num_sectors = FlashMap.total_flash_size/FlashMap.sector_size
        remaining_sectors = total_num_sectors
        sector_progress = ProgressLogger(self.logger, 0, total_num_sectors, msg="read")
        while remaining_sectors > 0:
            sector_progress.log(total_num_sectors-remaining_sectors)
            flash_data.extend(self.link.read_sector(flash_offset))
            flash_offset += FlashMap.sector_size
            remaining_sectors -= 1
        self.logger.info("Flash readback complete")
        return flash_data

    def _compare_binary_data(self, binary_one, binary_two):
        similar = True
        if len(binary_one) != len(binary_two):
            similar = False
            return similar
        for i in range(len(binary_one)):
            if binary_one[i] != binary_two[i]:
                similar = False
                return similar
        return similar

    def verify_flash(self, reference_data):
        flash_readback = self.read_flash()
        verify = self._compare_binary_data(reference_data, flash_readback)
        if verify is False:
            msg = "Verify failed"
            raise WincUpgradeError(msg)
        self.logger.debug("Verify successful")

    def upgrade_full_image(self, data):
        """
        Do the upgrade by erasing and writing
        """
        self.logger.info("WINC upgrade: erase")
        self.erase_flash()
        self.logger.info("WINC upgrade: write")
        self.write_flash(data)
        self.logger.info("WINC upgrade: verify")
        self.verify_flash(data)

    def _replace_sector(self, sector_offset, data):
        self.logger.debug("WINC upgrade: replace sector")
        self.erase_sector(sector_offset)
        self.write_sector(sector_offset, data)

    def write_tls_root_certificate_sector(self, data):
        sector_offset = FlashMap.tls_root_cert_offset
        if len(data) != FlashMap.tls_root_cert_size:
            raise WincUpgradeError("Invalid sector size")
        self._replace_sector(sector_offset, data)
        data_read = self.read_sector(sector_offset)
        if not self._compare_binary_data(data, data_read):
            msg = "Verify failed"
            raise WincUpgradeError(msg)
        self.logger.debug("Verify successful")
