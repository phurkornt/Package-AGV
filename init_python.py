import subprocess

files = ["navigation_node.py", "marker_node.py", "manager_node.py"]

for file in files:
    subprocess.call(["python", file])

