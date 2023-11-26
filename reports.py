import argparse
import os
import re
from datetime import datetime
from collections import defaultdict

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a report comparing two MegaKeep log files.')
    parser.add_argument('log1', nargs='?', help='Path to the first log file')
    parser.add_argument('log2', nargs='?', help='Path to the second log file')
    return parser.parse_args()

def find_recent_logs(log_dir, num_logs=2):
    log_files = [f for f in os.listdir(log_dir) if f.startswith('megakeep_') and f.endswith('.log')]
    # Adjusting the parsing of the filename to extract the date-time string correctly
    log_files.sort(key=lambda x: datetime.strptime(x[9:-4], "%Y-%m-%d_%H-%M-%S"), reverse=True)
    return [os.path.join(log_dir, f) for f in log_files[:num_logs]]

def parse_log_file(filepath):
    accounts_data = {}
    with open(filepath, 'r') as file:
        for line in file:
            if 'Account' in line:
                parts = line.split()
                email = parts[3]  # Extracting email
                
                # Manually parsing the space data
                space_data_str = line.split("Space used: ")[1].split(" MB")[0]
                used, total = space_data_str.replace("{", "").replace("}", "").replace("'", "").split(", ")
                used_val = float(used.split(": ")[1])
                total_val = float(total.split(": ")[1])
                
                accounts_data[email] = {'used': used_val, 'total': total_val}
    return accounts_data

def compare_logs(log_data1, log_data2):
    changes = {
        "added": [],
        "removed": [],
        "content_increased": [],
        "content_decreased": [],
        "unchanged": []
    }

    for email, data in log_data2.items():
        if email not in log_data1:
            changes["added"].append(email)
        elif log_data2[email]['used'] < log_data1[email]['used']:  # Inverted logic here
            changes["content_increased"].append(email)
        elif log_data2[email]['used'] > log_data1[email]['used']:  # And here
            changes["content_decreased"].append(email)
        else:
            changes["unchanged"].append(email)

    for email in log_data1:
        if email not in log_data2:
            changes["removed"].append(email)

    return changes

def generate_report(changes, log_data2):
    total_space_used = sum([data['used'] for data in log_data2.values()]) / 1024  # Convert to GB
    total_space_remaining = sum([data['total'] - data['used'] for data in log_data2.values()]) / 1024  # Convert to GB
    report_lines = [
        "MegaKeep Account Changes Report\n\n",
        f"Total space used: {total_space_used:.2f} GB\n",
        f"Total space available: {total_space_remaining:.2f} GB\n\n",
        "Summary:\n"
    ]
    
    # Summary with indentation and without underscores
    for category, emails in changes.items():
        category_name = category.replace("_", " ").title()
        if emails:  # Only add the category if there are emails
            report_lines.append(f"\t{category_name}: {len(emails)} accounts\n")

    # Detailed sections with indentation
    for category, emails in changes.items():
        if emails:  # Only add the category if there are emails
            category_name = category.replace("_", " ").title()
            report_lines.append(f"\n{category_name}:\n")
            for email in emails:
                space_used = (log_data2[email]['used'] / 1024) if email in log_data2 else 'N/A'  # Convert to GB
                space_remaining = ((log_data2[email]['total'] - log_data2[email]['used']) / 1024) if email in log_data2 else 'N/A'  # Convert to GB
                report_lines.append(f"\t{email} - Space used: {space_used:.2f} GB, Space remaining: {space_remaining:.2f} GB\n")

    return ''.join(report_lines)

def main():
    args = parse_arguments()
    log_dir = 'logs/raw'
    report_dir = 'logs/reports'

    if args.log1 and args.log2:
        log_files = [args.log1, args.log2]
    else:
        log_files = find_recent_logs(log_dir)

    log_data1 = parse_log_file(log_files[0])
    log_data2 = parse_log_file(log_files[1])

    changes = compare_logs(log_data1, log_data2)
    report = generate_report(changes, log_data2)
    
    # Extract just the dates from the log filenames
    date1 = os.path.basename(log_files[0])[9:-4].split('_')[0]
    date2 = os.path.basename(log_files[1])[9:-4].split('_')[0]
    
    report_filename = f"{report_dir}/change_report_{date1}_-_{date2}.txt"
    with open(report_filename, 'w') as f:
        f.write(report)
        
if __name__ == '__main__':
    main()
