
def print_flash_map():
    print("\nFlash offsets\n")
    print("--------------------")
    print("Start address: \t\t\t %d" %(FlashMap.start_addr))
    print("Boot firmware offset: \t\t %d" % (FlashMap.boot_fw_offset))
    print("Control section offset: \t %d" % (FlashMap.control_section_offset))
    print("PLL offset: \t\t\t %d" % (FlashMap.pll_offset))
    print("Gain offset: \t\t\t %d" % (FlashMap.gain_offset))
    print("TLS Root Certificate offset: \t %d" % (FlashMap.tls_root_cert_offset))
    print("TLS Server offset: \t\t %d" % (FlashMap.tls_server_offset))
    print("HTTP Files: \t\t\t %d" % (FlashMap.http_mem_offset))
    print("Cached connections: \t\t %d" % (FlashMap.cached_conns_offset))
    print("Firmware offset: \t\t %d" % (FlashMap.firmware_offset))
    print("OTA Firmware offset: \t\t %d" % (FlashMap.ota_fw_offset))

class FlashMap:
    start_addr = 0
    total_flash_size = 0x100000
    block_size = 32*1024
    page_size = 256
    sector_size = 4*1024

    boot_fw_offset = start_addr
    boot_fw_size = sector_size

    control_section_offset = boot_fw_offset + boot_fw_size
    control_section_size = sector_size*2

    pll_offset = control_section_offset + control_section_size
    pll_size = 1024
    gain_offset = pll_offset + pll_size
    gain_size = sector_size - pll_size

    tls_root_cert_offset = pll_offset + sector_size
    tls_root_cert_size = sector_size

    tls_server_offset = tls_root_cert_offset + tls_root_cert_size
    tls_server_size = sector_size * 2
    thing_name_offset = tls_server_offset + tls_server_size - page_size
    thing_name_size = 42
    aws_endpoint_offset = thing_name_offset - page_size

    http_mem_offset = tls_server_offset + tls_server_size
    http_mem_size = sector_size * 2

    cached_conns_offset = http_mem_offset + http_mem_size
    cached_conns_size = sector_size

    firmware_offset = cached_conns_offset + cached_conns_size
    firmware_size = 236 * 1024

    ota_fw_offset = firmware_offset + firmware_size
    ota_fw_size = firmware_size
