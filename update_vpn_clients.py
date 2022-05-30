from xml.etree import ElementTree
from shutil import copy
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import os

# Paths
config_path = "/conf/config.xml"
config_backup_path = "/conf/config.xml.bak"

# VPN settings
vpn_list = [
    {
        "target": "NordVPN Main",
        "port": "1194",
        "country": "81",
        "group": "legacy_standard",
        "technology": "openvpn_udp"
    },
    {
        "target": "NordVPN Fallback",
        "port": "443",
        "country": "81",
        "group": "legacy_standard",
        "technology": "openvpn_tcp"
    }
]


# Main runner
def run():

    # Make copy of config file
    if os.path.exists(config_path):
        copy(config_path, config_backup_path)
    else:
        print("Config file not found, stopping...")
        return

    # Load config file
    tree = ElementTree.parse(config_backup_path)
    root = tree.getroot()
    last_ip = None
    vpn_id_list = []

    # Go through VPN list to update entries
    for item in vpn_list:
        
        # Try to find config entry
        entry = root.find("./openvpn[openvpn-client]/*[description='" + item.get("target") + "']")
        
        if entry == None:
            print("Client entry not found, skipping...")
            continue
        
        # Request optimal VPN server from API
        last_ip = get_optimal_server(item.get("country"), item.get("group"), item.get("technology"), last_ip)
        
        # When an IP is received, update values
        if last_ip != None:
            entry.find("server_addr").text = last_ip
            entry.find("server_port").text = item.get("port")
            
            # Also mark VPN client for restart
            vpn_id_list.append(entry.find("vpnid").text)
        
    # Prevent further action if no VPN is marked
    if len(vpn_id_list) == 0:
        print("Nothing to do, stopping...")
        return
    
    # Save config
    tree.write(config_path)
    print("Config has been updated!")
    
    # Restart services
    for vpn_id in vpn_id_list:
        print("Restarting VPN with ID " + vpn_id + "...")
        os.system("pluginctl -s openvpn restart " + vpn_id)


# Requester for optimal server
def get_optimal_server(country, group, technology, exclude_ip):

    # Build request
    params = {
        "filters[country_id]": country,
        "filters[servers_groups][identifier]": group,
        "filters[servers_technologies][identifier]": technology,
        "limit": 3
    }
    
    # Perform request
    selected_ip = None
    
    try:
        request = urlopen("https://api.nordvpn.com/v1/servers/recommendations?" + urlencode(params))
        response = request.read()
        
        # Parse result & get best server
        parsed_response = json.loads(response)
        
        for server in parsed_response:
            server_ip = server.get("station")
            
            # Exclusion check
            if server_ip != exclude_ip:
                selected_ip = server_ip
                break
    except:
        print("API request failed...")
    
    # Return result
    return selected_ip


# Start script
run()