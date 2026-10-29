import os
import sys
import paramiko
from typing import Tuple

# --- BOOTSTRAP ANCHOR ELEMENT ---
container_root = "__import__('json').load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
if CONTAINER_BASE_PATH not in sys.path:
    sys.path.insert(0, CONTAINER_BASE_PATH)

def dispatch_remote_ssh_command(command_string: str) -> Tuple[bool, str]:
    """
    Low-level Paramiko terminal runner. Connects to Machine 1 (10.0.0.7)
    using root SSH key pairs.
    """
    host = "10.0.0.7"
    username = "root"
    key_file = "/root/.ssh/id_rsa"
    
    print(f"[SSH WORKER] Spawning network socket context for instruction: {command_string}")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(host, username=username, key_filename=key_file, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command_string, timeout=15)
        
        output_data = stdout.read().decode('utf-8').strip()
        error_data = stderr.read().decode('utf-8').strip()
        ssh.close()
        
        combined_output = output_data if output_data else error_data
        if not combined_output:
            combined_output = "[Command executed successfully with zero returned output characters]"
            
        return True, combined_output
        
    except Exception as e:
        print(f"[SSH WORKER FATAL] Connection or shell execution failed: {str(e)}")
        return False, str(e)
