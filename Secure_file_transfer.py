"""
Secure File Transfer
Copyright (C) 2023 Akash Pipaliya
This program is licensed under the MIT License.
See LICENSE for details.
"""

import os
import argparse
import paramiko
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser(description='Secure File Transfer')
    parser.add_argument('direction', choices=['send', 'recv'], help='Direction of transfer')
    parser.add_argument('source_path', type=str, help='Path of the source file/directory')
    parser.add_argument('destination_path', type=str, help='Path of the destination file/directory')
    parser.add_argument('--ip', type=str, default='localhost', help='IP address of the remote system')
    parser.add_argument('--port', type=int, default=22, help='SSH port of the remote system')
    parser.add_argument('--username', type=str, default=os.environ['USER'], help='Username of the remote system')
    parser.add_argument('--password', type=str, help='Password of the remote system')
    args = parser.parse_args()
    return args.direction, args.source_path, args.destination_path, args.ip, args.port, args.username, args.password


def connect(ip, port_ssh, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        ssh.connect(ip, port=port_ssh, username=username, password=password)
        print("\nConnected...........")
    except:
        print("Connection Error")
        print("Note: SSH port needs to be open on both the system")
        exit()
    return ssh


def transfer_file(sftp, direction, source_path, destination_path):
    if direction == "send":
        # Upload the file
        file = source_path.split("/")[-1]
        remote_path = os.path.join(destination_path, file)
        local_path = source_path
        with tqdm(total=os.stat(local_path).st_size, unit='B', unit_scale=True, desc=local_path) as progress_bar:
            sftp.put(local_path, remote_path,
                     callback=(lambda transferred, total: progress_bar.update(transferred - progress_bar.n)))
        print("\nFile Sent...........")
    elif direction == "recv":
        # Download the file
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


def main():
    direction, source_path, destination_path, ip, port, username, password = get_args()

    # Connect to the remote system
    ssh = connect(ip, port, username, password)

    # Start SFTP session
    sftp = ssh.open_sftp()

    # Upload or download the file
    transfer_file(sftp, direction, source_path, destination_path)

    # Close the connection
    sftp.close()
    ssh.close()


if __name__ == '__main__':
    main()
