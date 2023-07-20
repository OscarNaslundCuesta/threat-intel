import pandas as pd

# Read domains from domains.txt into a set
with open("domains.txt", "r") as f:
    legitimate_domains = set(line.strip() for line in f)

# Legitimate NS will be stored in this set
legitimate_ns = set()

# First pass: collect all legitimate nameservers from domains.txt
with open("dnstwist_output.txt", "r") as f:
    for line in f:
        words = line.split()
        if len(words) < 3:
            continue
        domain = words[1]
        if domain not in legitimate_domains:
            continue
        ns = None
        for word in words[2:]:
            if word.startswith("NS:"):
                ns = word.replace("NS:", "")
                break
        if ns is not None and ns != "!ServFail":
            legitimate_ns.add(ns)

# Raw data will be stored in a list of dictionaries, where each dictionary represents a row
data = []
# NS counts will be stored in this dictionary
ns_counts = {}

# Second pass: process all lines in file.txt
with open("dnstwist_output.txt", "r") as f:
    for line in f:
        words = line.split()
        if len(words) < 3:
            print(f"Skipping malformed line: {line}")
            continue
        domain = words[1]
        ns = None
        for word in words[2:]:
            if word.startswith("NS:"):
                ns = word.replace("NS:", "")
                break
        if ns is not None and ns != "!ServFail":
            legitimacy = "Legitimate" if ns in legitimate_ns else ""
            data.append({"Domain": domain, "NS": ns, "Legitimacy": legitimacy})
            if ns in ns_counts:
                ns_counts[ns] += 1
            else:
                ns_counts[ns] = 1
        else:
            print(f"Skipping line with no NS or with NS as !ServFail: {line}")

# Convert the data list and the ns_counts dictionary to pandas DataFrames
df_data = pd.DataFrame(data)
df_counts = pd.DataFrame([(ns, count, "Legitimate" if ns in legitimate_ns else "") for ns, count in ns_counts.items()],
                         columns=["Nameserver", "Count", "Legitimacy"])

# Write each DataFrame to a different worksheet in the same Excel file using 'xlsxwriter' engine
with pd.ExcelWriter("NS_Threat_Intel.xlsx", engine='xlsxwriter') as writer:
    df_data.to_excel(writer, sheet_name='Raw Data', index=False)
    df_counts.to_excel(writer, sheet_name='NS Counts', index=False)
