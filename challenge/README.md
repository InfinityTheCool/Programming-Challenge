# Intern Coding Challenge

Write a command-line program that reads a JSONL file from stdin and writes a JSON formatted summary of the data to stdout.

The command should produce a JSON document on standard out containing the below summary information. You may choose the 
JSON structure you'd like to use for the output.

## Questions

### Device Summary:

1. Total number of devices
2. What are the top 10 most common services that devices use?
3. For the HTTP(port 80) banners, what's the median, average, and 90th percentile banner lengths?
4. List the 5 most common HTTP headers used by each Web server type


Here's a quick summary of the relevant input fields in the input file for this exercise:

1. id - the UUIDv4 of the device in the system
2. addr - the IPv4 of the device
3. lastScan - this is sub json structure which contains the most recent scan data of the device. 
This is where you will find the different services that each device exposes. For example, the key "10.81.3.61/80/tcp/" 
means there is a service running on port 80. The JSON value for that key will further describe that service. The "protocol" 
field contains the protocol running on that port. Protocol values of "http" and "https" are what you should use for finding 
web servers. The banner field is what you should use to find the HTTP Headers for each server. The server type may be found 
in the field "service.cpe23".

The full scan format may be found under the "Asset data" section of https://www.rumble.run/docs/data-formats/

Please use a scripting language for this challenge, such as Python.

## Project structure

We have provided a skeleton to build and run this program. Please use the Makefile and Dockerfile to run this program 
(make any modifications to them that you need to). 

With the initial skeleton setup, running `make run` will build the docker image and run the script in src/summarize.py. 
It will also install any dependencies that you need (put those in requirements.txt). You may need to install Docker first. 
Feel free to add any command-line flags or other items you might find helpful.



