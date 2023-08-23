import os
import time
import csv

def get_workspace_info(root_dir):
    workspace_info = []

    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name.startswith('j07') or dir_name.startswith('j04'):
                workspace_path = os.path.join(root, dir_name)
                workspace_name = workspace_path.split('/')[-1]
                
                created_time = time.ctime(os.path.getctime(workspace_path))
                accessed_time = time.ctime(os.path.getatime(workspace_path))
                size_on_disk = os.path.getsize(workspace_path) // (1024 * 1024)  # in MB
                
                provisioned_space = os.statvfs(workspace_path).f_blocks * os.statvfs(workspace_path).f_frsize // (1024 * 1024)  # in MB
                
                workspace_info.append({
                    'name': workspace_name,
                    'created_time': created_time,
                    'accessed_time': accessed_time,
                    'size_on_disk': size_on_disk,
                    'provisioned_space': provisioned_space
                })

                print(f"Processed: {workspace_path}")

    return workspace_info

def write_to_file(workspace_info, output_file):
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['Name', 'Created Time', 'Last Accessed Time', 'Size on Disk (MB)', 'Provisioned Space (MB)']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for info in workspace_info:
            writer.writerow(info)

if __name__ == "__main__":
    root_directory = "/gws"  # Change this to your root directory
    output_filename = "workspace_info.csv"

    workspace_info = get_workspace_info(root_directory)
    write_to_file(workspace_info, output_filename)
    print(f"Workspace information has been written to {output_filename}")
