#!/bin/bash

# Ensure dnstwist is installed
if ! command -v dnstwist &> /dev/null
then
    echo "dnstwist could not be found, please install it."
    exit
fi

# Check if domains.txt exists
if [ ! -f domains.txt ]; then
    echo "File domains.txt not found!"
    exit 1
fi

# Read the file line by line
while read -r domain; do
    echo "Processing $domain"
    dnstwist -r "$domain" >> dnstwist_output.txt
done < "domains.txt"

