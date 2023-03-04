# **Secure File Transfer**

This Python script uses Paramiko library to transfer files securely between local and remote systems using SFTP protocol.

------------
Usage:
------------
python3 secure_file_transfer.py <direction> <source_path> <destination_path> [--ip <ip>] [--port <port>] [--username <username>] [--password <password>]


------------------------------------------------------------
The script takes the following positional arguments:
------------------------------------------------------------
direction: Direction of transfer. It can be send to upload a file from local system to remote system, or recv to download a file from remote system to local system.

source_path: Path of the source file/directory.

destination_path: Path of the destination file/directory.


--------------------------------------------------------------
The script also takes the following optional arguments:
--------------------------------------------------------------
--ip: IP address of the remote system. Default is localhost.

--port: SSH port of the remote system. Default is 22.

--username: Username of the remote system. Default is current user.

--password: Password of the remote system. If not provided, the script will attempt to use SSH keys.

-------------
Dependencies
-------------
The script requires the following Python libraries:

argparse

os

paramiko (pip install paramiko)

tqdm (pip install tqdm)

------------------------------------------------
To upload a local file to a remote system:
------------------------------------------------
python3 secure_file_transfer.py send /path/to/local/file.txt /path/to/remote/directory

------------------------------------------------
To download a remote file to a local system:
------------------------------------------------
python3 secure_file_transfer.py recv /path/to/remote/file.txt /path/to/local/directory

-----------------------------------------------------------------
To specify a remote IP address, SSH port, username and password:
-----------------------------------------------------------------
python3 secure_file_transfer.py send /path/to/local/file.txt /path/to/remote/directory --ip 192.168.1.100 --port 2222 --username john --password secret
