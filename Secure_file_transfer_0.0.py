import paramiko
# from scp import SCPClient
from tqdm import tqdm
import sys
import os

# =============================================================================================================================================
# CLI error handling
if len(sys.argv) < 2:
    print("Fatal: No arguments provided ")
    print("try --> python3 SCP.py [Remote IP] [SSH Port] [Remote Username] [Remote password] [-send/-recv] [source_path] [destination_path]")
    exit()
elif (len(sys.argv) < 8 or len(sys.argv) > 8) and sys.argv[1] != "-h":
    print("No. of arguments provided are invalid")
    print("try --> python3 SCP.py [Remote IP] [SSH Port] [Remote Username] [Remote password] [-send/-recv] [source_path] [destination_path]")
    exit()

if sys.argv[1] == "-h":
    print(
        '''
    try --> python3 SCP.py [Remote IP] [SSH Port] [Remote Username] [Remote password] [-send/-recv] [source_path] [destination_path]

    Note: SSH port needs to be open on both the system

    [Remote IP]         = IP Address of Remote device/system
    [SSH Port]          = SSH Port number (default 22)
    [Remote Username]   = Username of Remote system
    [Remote Password]   = Password of remote system
    [-send/-recv]       = Type of operation (Send or Receive file)
    [source_path]       = Absolute path of the file to be transferred
    [Destination_path]  = Path where file needs to be received
        '''
    )
    exit()
else:
    pass

# CLI Arguments
ip = sys.argv[1]
port_ssh = int(sys.argv[2])
username = str(sys.argv[3])
password = str(sys.argv[4])
direction = sys.argv[5]
source_path = str(sys.argv[6])
destination_path = str(sys.argv[7])

# SSH connect
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
try:
    ssh.connect(f'{ip}', port=port_ssh, username=f'{username}', password=f'{password}')
    print("\nConnected...........")

except:
    print("Connection Error")
    print("Note: SSH port needs to be open on both the system")
    exit()

# Start SFTP session
sftp = ssh.open_sftp()

# Direction to file transfer
if direction == "-send":
    file = source_path.split("/")[-1]
    remote_path = os.path.join(destination_path, file)
    local_path = source_path
    with tqdm(total=os.stat(local_path).st_size, unit='B', unit_scale=True, desc=local_path) as progress_bar:
        sftp.put(local_path, remote_path,
                 callback=(lambda transferred, total: progress_bar.update(transferred - progress_bar.n)))
    print("\nFile Sent...........")

elif direction == "-recv":
    file = source_path.split("/")[-1]
    file_path = source_path.strip(file)
    remote_path = os.path.join(file_path, file)
    local_path = os.path.join(destination_path, file)
    # Get the size of the remote file
    remote_size = sftp.stat(remote_path).st_size
    with tqdm(total=remote_size, unit='B', unit_scale=True, desc=remote_path) as progress_bar:
        sftp.get(remotepath=remote_path, localpath=local_path,
                 callback=(lambda transferred, total: progress_bar.update(transferred - progress_bar.n)))
    print("\nFile Received...........")

# Closing the connection
sftp.close()
ssh.close()

