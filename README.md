# Setup
1. Copy the .py and .conf file to somewhere on your system, like your home folder
2. Note the absolute path of the .py file (needed for the cron step)

# Main configuration
3. Open the python file and look for the "vpn_list" variable
4. Change the "target" fields to your OpenVPN client description values
5. Modify the other fields to your requirements
     - For countries (use ID values): https://github.com/azinchen/nordvpn/blob/master/COUNTRIES.md 
     - For groups (use identifier values): https://github.com/azinchen/nordvpn/blob/master/GROUPS.md
     - For technologies (use identifier values): https://github.com/azinchen/nordvpn/blob/master/TECHNOLOGIES.md
     - You can add/remove more objects to the array, depending on your needs
6. Save the file

# Cron integration
7. Open actions_nordvpn.conf and update the "parameters" field with the absolute path of the .py file from step 2
8. Copy actions_nordvpn.conf to the /usr/local/opnsense/service/conf/actions.d folder
9. Run "sudo service configd restart" to apply
10. Run "sudo configctl nordvpn start" to check if it works correctly
     - It should return "OK", if not please make sure the paths in the .conf file are correct
     - If it still doesn't work, you can try to manually execute the script to see what is wrong
     - Manual execution example: sudo /usr/local/bin/python3 /home/admin/vpn/update_vpn_clients.py
11. If you want more verbose output, you can change the "type" value in the .conf file to "script_output"
12. If everything is okay, you can make a cron entry via the GUI!