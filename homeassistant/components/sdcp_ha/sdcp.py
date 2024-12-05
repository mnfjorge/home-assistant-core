
import asyncio
import json
import logging
import socket

from .const import DISCOVERY_TIMEOUT


logger = logging.getLogger(__name__)

async def discover_printers():
  logger.info("Starting printer discovery.")
  msg = b'M99999'
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  sock.settimeout(DISCOVERY_TIMEOUT)
  sock.bind(("", 54781))
  sock.sendto(msg, ("255.255.255.255", 3000))
  socketOpen = True
  printers = []
  while (socketOpen):
    try:
        data = sock.recv(8192)
        printer = get_printer_data(data)
        printers[printer['mainboardID']] = printer
        logger.info("Discovered: {n} ({i})".format(n=printer['name'], i=printer['ip']))
    except TimeoutError:
        logger.info("Discovery timeout")
        sock.close()
        break

  logger.info("Discovery done.")
  return printers


def get_printer_data(data: bytes):
  j = json.loads(data.decode('utf-8'))
  printer = {}
  printer['connection'] = j['Id']
  printer['name'] = j['Data']['Name']
  printer['model'] = j['Data']['MachineName']
  printer['brand'] = j['Data']['BrandName']
  printer['ip'] = j['Data']['MainboardIP']
  printer['mainboardID'] = j['Data']['MainboardID']
  printer['protocol'] = j['Data']['ProtocolVersion']
  printer['firmware'] = j['Data']['FirmwareVersion']
  return printer
