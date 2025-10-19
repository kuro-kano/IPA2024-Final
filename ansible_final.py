import subprocess
import os

def showrun():

    ansible_dir = os.path.join(os.path.dirname(__file__), 'ansible')
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ["ansible-playbook", "playbook.yaml"]
    result = subprocess.run(command, capture_output=True, text=True, cwd=ansible_dir)
    result = result.stdout

    if 'ok=2' in result:
        return 'ok'
    else:
        return 'Error: Ansible'
