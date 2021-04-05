"""Utilities to help CANU cache switch information to YAML."""

import datetime
from operator import itemgetter
import os.path
import sys

import pkg_resources
import ruamel.yaml


yaml = ruamel.yaml.YAML()

# To get the canu_cache.yaml file in the parent directory
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):  # pragma: no cover
    parent_directory = sys._MEIPASS
else:
    prog = __file__
    current_directory = os.path.dirname(os.path.abspath(prog))
    parent_directory = os.path.split(current_directory)[0]

canu_cache_file = os.path.join(parent_directory, "canu_cache.yaml")

file_exists = os.path.isfile(canu_cache_file)

# Open the Cache file, and generate it if it does not exist
if file_exists:  # pragma: no cover
    with open(canu_cache_file, "r+") as file:
        canu_cache = yaml.load(file)
else:  # pragma: no cover
    version = pkg_resources.require("canu")[0].version
    with open(canu_cache_file, "w+") as f:
        f.write(f"version: {version}\n")
        f.write("switches:\n")

    with open(canu_cache_file, "r+") as file:
        canu_cache = yaml.load(file)


def cache_switch(switch):
    """Cache a switch.

    The switch that is passed in will either be added to the cache, or updated in the cache, depending on if it existed before.

    :param switch: The JSON switch object to be added to the cache.

    The updated cache is immediately written to a file.
    """
    if ip_exists_in_cache(switch["ip_address"]):
        updated_cache = update_switch_in_cache(canu_cache, switch)
    else:
        updated_cache = add_switch_to_cache(canu_cache, switch)

    with open(canu_cache_file, "w") as f:
        yaml.dump(updated_cache, f)


def cached_recently(ip, max_cache_time=10):
    """Check if a switch has recently been cached and return True or False.

    :param ip: The IPv4 address to check in the cache.

    :param max_cache_time: Optional parameter (defaults to 10) to determine the maximum cache time in minutes.

    :return: True or False depending on if the IP address has been cached less than the max_cache_time parameter.
    """
    if ip_exists_in_cache(ip):
        index = list(map(itemgetter("ip_address"), canu_cache["switches"])).index(ip)
        time_now = datetime.datetime.now()

        cache_time = datetime.datetime.strptime(
            canu_cache["switches"][index]["updated_at"], "%Y-%m-%d %H:%M:%S"
        )

        time_difference = time_now - cache_time
        time_difference_minutes = time_difference.total_seconds() / 60

        if time_difference_minutes < max_cache_time:
            return True

    return False


def get_switch_from_cache(ip):
    """Return an existing switch from the cache by IP lookup.

    :param ip: The IPv4 address of the switch to be retrieved from the cache.

    :return: The JSON switch from the cache.
    """
    if ip_exists_in_cache(ip):
        index = list(map(itemgetter("ip_address"), canu_cache["switches"])).index(ip)
        return canu_cache["switches"][index]
    else:
        raise Exception(f"IP address {ip} not in cache.")


def update_switch_in_cache(cache, switch):
    """Update an existing switch in the cache.

    :param cache: The JSON representation of the current YAML cache file.

    :param switch: The JSON switch object to be added to the cache.

    :return: The updated JSON cache with the switch updated.
    """
    index = list(map(itemgetter("ip_address"), cache["switches"])).index(
        switch["ip_address"]
    )
    for attribute in switch:
        cache["switches"][index][attribute] = switch[attribute]

    return cache


def add_switch_to_cache(cache, switch):
    """Add a switch to the cache.

    :param cache: The JSON representation of the current YAML cache file.

    :param switch: The JSON switch object to be added to the cache.

    :return: The updated JSON cache with the switch appended
    """
    # If there are no switches yet in the cache
    if cache["switches"] is None:  # pragma: no cover
        cache["switches"] = [switch]
    else:
        cache["switches"].append(switch)

    return cache


def remove_switch_from_cache(ip):
    """Remove a switch from the cache.

    This function is useful for removing a test switch from the cache.

    :param cache: The JSON representation of the current YAML cache file.

    :param switch: The JSON switch object to be added to the cache.

    :return: The updated JSON cache with the switch appended
    """
    index = list(map(itemgetter("ip_address"), canu_cache["switches"])).index(ip)

    updated_cache = canu_cache
    updated_cache["switches"].pop(index)

    with open(canu_cache_file, "w") as f:
        yaml.dump(updated_cache, f)

    return


def ip_exists_in_cache(ip):
    """Check if a switch already exists in the cache.

    :param ip: The IPv4 address to check.

    :return: True or False depending on if the IP address is in the cache.
    """
    if canu_cache["switches"] is not None and ip in map(
        itemgetter("ip_address"), canu_cache["switches"]
    ):
        return True
    return False
