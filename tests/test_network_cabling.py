"""Test CANU switch firmware commands."""

import click.testing
import requests
import responses

from canu.cli import cli


username = "admin"
password = "admin"
ip = "192.168.1.1"
ips = "192.168.1.1"
credentials = {"username": username, "password": password}
cache_minutes = 0
runner = click.testing.CliRunner()


@responses.activate
def test_network_cabling():
    """Test that the `canu network cabling` command runs and returns valid cabling."""
    with runner.isolated_filesystem():
        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/login",
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system?attributes=platform_name,hostname,system_mac",
            json=switch_info1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/interfaces/*/lldp_neighbors?depth=2",
            json=lldp_neighbors_json1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/vrfs/default/neighbors?depth=2",
            json=arp_neighbors_json1,
        )

        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/logout",
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips",
                ips,
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 0
        assert "1/1/1   ==> sw-test02      1/1/1" in str(result.output)


@responses.activate
def test_network_cabling_file():
    """Test that the `canu network cabling` command runs from a file input and returns valid cabling."""
    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("192.168.1.1")

        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/login",
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system?attributes=platform_name,hostname,system_mac",
            json=switch_info1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/interfaces/*/lldp_neighbors?depth=2",
            json=lldp_neighbors_json1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/vrfs/default/neighbors?depth=2",
            json=arp_neighbors_json1,
        )

        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/logout",
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips-file",
                "test.txt",
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 0
        assert "1/1/1   ==> sw-test02      1/1/1" in str(result.output)


@responses.activate
def test_network_cabling_file_bidirectional():
    """Test that the `canu network cabling` command runs from a file input and returns valid cabling."""
    ip2 = "192.168.1.2"
    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("192.168.1.1\n")
            f.write(ip2)

        # Switch 2
        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/login",
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system?attributes=platform_name,hostname,system_mac",
            json=switch_info1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/interfaces/*/lldp_neighbors?depth=2",
            json=lldp_neighbors_json1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/vrfs/default/neighbors?depth=2",
            json=arp_neighbors_json1,
        )

        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/logout",
        )

        # Switch 2
        responses.add(
            responses.POST,
            f"https://{ip2}/rest/v10.04/login",
        )
        responses.add(
            responses.GET,
            f"https://{ip2}/rest/v10.04/system?attributes=platform_name,hostname,system_mac",
            json=switch_info2,
        )
        responses.add(
            responses.GET,
            f"https://{ip2}/rest/v10.04/system/interfaces/*/lldp_neighbors?depth=2",
            json=lldp_neighbors_json2,
        )
        responses.add(
            responses.GET,
            f"https://{ip2}/rest/v10.04/system/vrfs/default/neighbors?depth=2",
            json=arp_neighbors_json2,
        )

        responses.add(
            responses.POST,
            f"https://{ip2}/rest/v10.04/logout",
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips-file",
                "test.txt",
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 0
        assert "1/1/1   ==> sw-test02      1/1/1" in str(result.output)


@responses.activate
def test_network_cabling_equipment_view():
    """Test that the `canu network cabling` command runs and returns valid cabling."""
    with runner.isolated_filesystem():
        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/login",
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system?attributes=platform_name,hostname,system_mac",
            json=switch_info1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/interfaces/*/lldp_neighbors?depth=2",
            json=lldp_neighbors_json1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/vrfs/default/neighbors?depth=2",
            json=arp_neighbors_json1,
        )

        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/logout",
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips",
                ips,
                "--username",
                username,
                "--password",
                password,
                "--view",
                "equipment",
            ],
        )
        assert result.exit_code == 0
        assert "11:11:11:11:11:11         <=== sw-test01       1/1/3" in str(
            result.output
        )


@responses.activate
def test_network_cabling_file_equipment_view_bidirectional():
    """Test that the `canu network cabling` command runs from a file input and returns valid cabling."""
    ip2 = "192.168.1.2"
    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("192.168.1.1\n")
            f.write(ip2)

        # Switch 1
        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/login",
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system?attributes=platform_name,hostname,system_mac",
            json=switch_info1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/interfaces/*/lldp_neighbors?depth=2",
            json=lldp_neighbors_json1,
        )
        responses.add(
            responses.GET,
            f"https://{ip}/rest/v10.04/system/vrfs/default/neighbors?depth=2",
            json=arp_neighbors_json1,
        )

        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/logout",
        )
        # Switch 2
        responses.add(
            responses.POST,
            f"https://{ip2}/rest/v10.04/login",
        )
        responses.add(
            responses.GET,
            f"https://{ip2}/rest/v10.04/system?attributes=platform_name,hostname,system_mac",
            json=switch_info2,
        )
        responses.add(
            responses.GET,
            f"https://{ip2}/rest/v10.04/system/interfaces/*/lldp_neighbors?depth=2",
            json=lldp_neighbors_json2,
        )
        responses.add(
            responses.GET,
            f"https://{ip2}/rest/v10.04/system/vrfs/default/neighbors?depth=2",
            json=arp_neighbors_json2,
        )

        responses.add(
            responses.POST,
            f"https://{ip2}/rest/v10.04/logout",
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips-file",
                "test.txt",
                "--username",
                username,
                "--password",
                password,
                "--view",
                "equipment",
            ],
        )
        assert result.exit_code == 0
        assert "11:11:11:11:11:11         <=== sw-test01       1/1/3" in str(
            result.output
        )


def test_network_cabling_missing_ips():
    """Test that the `canu network cabling` command errors on missing IP address."""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 2
        assert (
            "Error: Missing one of the required mutually exclusive options from 'Network cabling IPv4 input sources' option group"
            in str(result.output)
        )


def test_network_cabling_mutually_exclusive_ips_and_file():
    """Test that the `canu network cabling` command only accepts IPs from command line OR file input, not both."""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--username",
                username,
                "--password",
                password,
                "--ips",
                ips,
                "--ips-file",
                "file.txt",
            ],
        )
        assert result.exit_code == 2
        assert (
            "Error: Mutually exclusive options from 'Network cabling IPv4 input sources'"
            in str(result.output)
        )


def test_network_cabling_invalid_ip():
    """Test that the `canu network cabling` command errors on invalid IP address."""
    invalid_ip = "999.999.999.999"

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips",
                invalid_ip,
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 2
        assert (
            "Error: Invalid value for '--ips': These items are not ipv4 addresses: ['999.999.999.999']"
            in str(result.output)
        )


def test_network_cabling_invalid_ip_file():
    """Test that the `canu network cabling` command errors on invalid IPs from a file."""
    invalid_ip = "999.999.999.999"

    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write(invalid_ip)

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips-file",
                "test.txt",
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 2
        assert "Error: Invalid value:" in str(result.output)


@responses.activate
def test_network_cabling_bad_ip():
    """Test that the `canu network cabling` command errors on bad IP address."""
    bad_ip = "192.168.1.99"

    with runner.isolated_filesystem():
        responses.add(
            responses.POST,
            f"https://{bad_ip}/rest/v10.04/login",
            body=requests.exceptions.ConnectionError(
                "Failed to establish a new connection: [Errno 60] Operation timed out'))"
            ),
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips",
                bad_ip,
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 0
        assert "check the IP address and try again" in str(result.output)


@responses.activate
def test_network_cabling_bad_ip_file():
    """Test that the `canu network cabling` command errors on a bad IP from a file."""
    bad_ip = "192.168.1.99"

    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write(bad_ip)

        responses.add(
            responses.POST,
            f"https://{bad_ip}/rest/v10.04/login",
            body=requests.exceptions.ConnectionError(
                "Failed to establish a new connection: [Errno 60] Operation timed out'))"
            ),
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips-file",
                "test.txt",
                "--username",
                username,
                "--password",
                password,
            ],
        )
        assert result.exit_code == 0
        assert "check the IP address and try again" in str(result.output)


@responses.activate
def test_network_cabling_bad_password():
    """Test that the `canu network cabling` command errors on bad credentials."""
    bad_password = "foo"

    with runner.isolated_filesystem():
        responses.add(
            responses.POST,
            f"https://{ip}/rest/v10.04/login",
            body=requests.exceptions.HTTPError("Client Error: Unauthorized for url"),
        )

        result = runner.invoke(
            cli,
            [
                "--cache",
                cache_minutes,
                "network",
                "cabling",
                "--ips",
                ip,
                "--username",
                username,
                "--password",
                bad_password,
            ],
        )
        assert result.exit_code == 0
        assert "check the username or password" in str(result.output)


# Switch 1
switch_info1 = {
    "hostname": "sw-test01",
    "platform_name": "X86-64",
    "system_mac": "aa:aa:aa:aa:aa:aa",
}

lldp_neighbors_json1 = {
    "1%2F1%2F1": {
        "bb:bb:bb:bb:bb:bb,1/1/1": {
            "chassis_id": "bb:bb:bb:bb:bb:bb",
            "mac_addr": "bb:bb:bb:bb:bb:cc",
            "neighbor_info": {
                "chassis_description": "Test switch description",
                "chassis_name": "sw-test02",
                "port_description": "1/1/1",
                "port_id_subtype": "if_name",
            },
            "port_id": "1/1/1",
        }
    },
    "1%2F1%2F2": {
        "bb:bb:bb:bb:bb:cc,1/1/2": {
            "chassis_id": "bb:bb:bb:bb:bb:bb",
            "mac_addr": "bb:bb:bb:bb:bb:cc",
            "neighbor_info": {
                "chassis_description": "Test switch description",
                "chassis_name": "sw-test02",
                "port_description": "1/1/2",
                "port_id_subtype": "if_name",
            },
            "port_id": "1/1/2",
        }
    },
    "1%2F1%2F3": {
        "00:00:00:00:00:00,00:00:00:00:00:00": {
            "chassis_id": "00:00:00:00:00:00",
            "mac_addr": "00:00:00:00:00:00",
            "neighbor_info": {
                "chassis_description": "",
                "chassis_name": "",
                "port_description": "",
                "port_id_subtype": "link_local_addr",
            },
            "port_id": "00:00:00:00:00:00",
        },
        "11:11:11:11:11:11,11:11:11:11:11:11": {
            "chassis_id": "11:11:11:11:11:11",
            "mac_addr": "11:11:11:11:11:11",
            "neighbor_info": {
                "chassis_description": "",
                "chassis_name": "",
                "port_description": "",
                "port_id_subtype": "link_local_addr",
            },
            "port_id": "11:11:11:11:11:11",
        },
    },
    "1%2F1%2F4": {
        "cc:cc:cc:cc:cc:cc,cc:cc:cc:cc:cc:cc": {
            "chassis_id": "cc:cc:cc:cc:cc:cc",
            "mac_addr": "cc:cc:cc:cc:cc:cc",
            "neighbor_info": {
                "chassis_description": "NCN description",
                "chassis_name": "ncn-test",
                "port_description": "mgmt1",
                "port_id_subtype": "link_local_addr",
            },
            "port_id": "cc:cc:cc:cc:cc:cc",
        }
    },
}

arp_neighbors_json1 = {
    "192.168.1.2,vlan1": {
        "mac": "00:00:00:00:00:00",
        "ip_address": "192.168.1.2",
        "port": {"vlan1": "/rest/v10.04/system/interfaces/vlan1"},
    },
    "192.168.1.3,vlan2": {
        "mac": "11:11:11:11:11:11",
        "ip_address": "192.168.1.3",
        "port": {"vlan2": "/rest/v10.04/system/interfaces/vlan2"},
    },
    "192.168.2.2,vlan3": {
        "mac": "00:00:00:00:00:00",
        "ip_address": "192.168.2.2",
        "port": {"vlan3": "/rest/v10.04/system/interfaces/vlan3"},
    },
}

# Switch 2
switch_info2 = {
    "hostname": "sw-test02",
    "platform_name": "X86-64",
    "system_mac": "bb:bb:bb:bb:bb:bb",
}

lldp_neighbors_json2 = {
    "1%2F1%2F1": {
        "aa:aa:aa:aa:aa:aa,1/1/1": {
            "chassis_id": "aa:aa:aa:aa:aa:aa",
            "mac_addr": "aa:aa:aa:aa:aa:aa",
            "neighbor_info": {
                "chassis_description": "Test switch description",
                "chassis_name": "sw-test01",
                "port_description": "",
                "port_id_subtype": "if_name",
            },
            "port_id": "1/1/1",
        }
    },
    "1%2F1%2F2": {
        "aa:aa:aa:aa:aa:bb,1/1/2": {
            "chassis_id": "aa:aa:aa:aa:aa:aa",
            "mac_addr": "aa:aa:aa:aa:aa:bb",
            "neighbor_info": {
                "chassis_description": "Test switch description",
                "chassis_name": "sw-test01",
                "port_description": "",
                "port_id_subtype": "if_name",
            },
            "port_id": "1/1/2",
        }
    },
}

arp_neighbors_json2 = {
    "192.168.1.2,vlan1": {
        "mac": "00:00:00:00:00:00",
        "ip_address": "192.168.1.2",
        "port": {"vlan1": "/rest/v10.04/system/interfaces/vlan1"},
    },
    "192.168.1.3,vlan2": {
        "mac": "11:11:11:11:11:11",
        "ip_address": "192.168.1.3",
        "port": {"vlan2": "/rest/v10.04/system/interfaces/vlan2"},
    },
    "192.168.2.2,vlan3": {
        "mac": "00:00:00:00:00:00",
        "ip_address": "192.168.2.2",
        "port": {"vlan3": "/rest/v10.04/system/interfaces/vlan3"},
    },
}
