#!/usr/bin/env python3

"""Send a JSON object to stdout containing the total number of devices,
most common services, median average and 90th percentile banner length,
and most common HTTP headers.
"""

# Written by Dennis Parkman
# 3/30/2021
# Internship Technical Challenge

# Imports
import json
import fileinput
import sys
import math

# Constants
CONST_COMMON_SERVICE_COUNT = 10
CONST_COMMON_HEADER_COUNT = 5

# Variables used to track data
total_devices=0
services = {}
headers = {}
banners = []

# Check for file path provided
try:
    arg1 = sys.argv[1]
except IndexError:
    print("No File Path Provided")
    sys.exit(1)

# Iterate through lines of json input
for line in fileinput.input():

    # Count devices
    total_devices+=1

    # Read JSON object into dict
    device = json.loads(line)

    # Get services and dict that represents sub json structure of service
    for service, service_dict in device["lastScan"]["data"]["services"].items():

        #Check for HTTP program
        if "protocol" in service_dict:
            protocol = service_dict["protocol"]
            if protocol == "http":

                # Track HTTP Banners
                banner = service_dict["banner"]
                banners.append(banner)

                # Filter out request data before and banner data after headers
                request, headers_and_doctype = banner.split('\n', 1)
                try:
                    headers_and_doctype.index('\r\n\r\n')
                    headers_in_banner, doctype_info = headers_and_doctype.split('\r\n\r\n', 1)
                except ValueError:
                    headers_in_banner = headers_and_doctype

                # Get HTTP headers
                found_headers = headers_in_banner.split('\r\n')
                for header in found_headers:
                    header = header.split(":")[0]
                    header = header.lower()
                    # Track most common HTTP headers
                    if header in headers:
                        headers[header] += 1
                    else:
                        headers[header] = 1

        # Get service to track most common services (port + protocol)
        serv = service.split("/")

        # Ignore ICMP local ping
        if serv[1] is not "0" and serv[2] is not "icmp":
            service = serv[1] + "/" + serv[2]
            if service in services:
                services[service] += 1
            else:
                services[service] = 1

# Total number of devices already held in total_devices

# List to hold most common services
common_services = []

# Sort by count to get list of most common HTTP headers used by each web service type
sorted_services = sorted(services.items(), key=lambda x: x[1], reverse=True)
for i in range(CONST_COMMON_SERVICE_COUNT):
    service = sorted_services[i]
    common_services.append((service[0], service[1]))

# Banner variables
banner_total_length = 0
banner_count = 0

# Sort banner by length to calculate median and 90th percentile
sorted_banners = sorted(banners, key=lambda x: len(x))
# Iterate through banners
for banner in sorted_banners:
    banner_count += 1
    banner_total_length += len(banner)

# Calculate median
banner_median_count = banner_count/2
if banner_median_count.is_integer():
    banner_median = len(sorted_banners[int(banner_median_count)])
else:
    banner_median_count = math.ceil(banner_median_count)
    banner_median = len(sorted_banners[banner_median_count - 1], sorted_banners[banner_median_count])

# Calculate average banner length
banner_average_length = banner_total_length / banner_count

# Find 90th percentile
banner_ninetieth_percentile_count = math.ceil(banner_count * 0.9)
banner_ninetieth_percentile = len(sorted_banners[banner_ninetieth_percentile_count])

# List to hold most common headers
common_headers = []

# Sort by count to get list of most common services used by devices
sorted_headers = sorted(headers.items(), key=lambda x: x[1], reverse=True)
for i in range(CONST_COMMON_HEADER_COUNT):
    header = sorted_headers[i]
    common_headers.append((header[0], header[1]))

summary =\
{
    "totalDevices": total_devices,
    "commonServices":common_services,
    "bannerMedianLength":banner_median,
    "bannerAverageLength":banner_average_length,
    "bannerNinetiethPercentileLength":banner_ninetieth_percentile,
    "commonHeaders":common_headers
}

sys.stdout.write(json.dumps(summary))