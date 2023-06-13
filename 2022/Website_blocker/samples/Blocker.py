import os
import re
import logging

#Log config
logging.basicConfig(filename="log.txt", filemode='a', level=logging.DEBUG)
logger = logging.getLogger('Blocker')

block_list = []
hosts_file_path = "..\\hosts.old"

try:
    size_of_file = os.stat(hosts_file_path).st_size
except FileNotFoundError as fnfe:
    logger.warning(fnfe)
    logger.warning("***The file does not exist or is not correctly spelled!***")


def checking_for_ip(ip):
    ip_regex = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if re.match(pattern=ip_regex, string=ip):
        if len([x for x in ip.split(".") if int(x) > 255]) == 0:
            return True
        else:
            return False
    else:
        return False

def reading_host_file():
    try:
        with open (hosts_file_path, "r") as host_file:
            file_content = host_file.read()
            return file_content
    except FileNotFoundError as fnfe:
        logger.warning(fnfe)
        logger.warning("***The file does not exist or is not correctly spelled!!***")

def modifying_host_file(string_to_add):
    try:
        with open (hosts_file_path, "a") as host_file:
            host_file.write(str(string_to_add))
            return
    except FileNotFoundError as fnfe:
        logger.warning(fnfe)
        logger.warning("The file does not exist or is not correctly spelled!!")


def clear_host_file_as_if_not_touched():
    try:
        with open(hosts_file_path, "r+") as host_file:
            host_file.seek(0,0)
            return host_file.truncate(size_of_file)
    except FileNotFoundError as fnfe:
        logger.warning(fnfe)
        logger.warning("The file does not exist or is not correctly spelled!!")

"""
Class that'll contain all the program, we'll add a site from here and delete a site from here
@param param1: localhost, or address where the site gonna be redirected 
"""
class Blocker():
    def __init__(self, localhost):
        self.localhost = localhost

    def adding_site(self, site):
        if site.startswith("www."):
            block_list.append(site)
            modifying_host_file(self.localhost + " " + site)
            print("Added", site)
            return block_list

        if checking_for_ip(site):
            block_list.append(site)
            modifying_host_file(self.localhost + " " + site)
            print("Added", site)
            return block_list
        else:
            return -1


    def deleting_site(self, site):
        if site in block_list:
            block_list.remove(site)
            print("Deleted", site)
        pass
