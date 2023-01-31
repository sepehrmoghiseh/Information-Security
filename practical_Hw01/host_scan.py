import argparse
import nmap

parser = argparse.ArgumentParser(prog="my-host-scan", allow_abbrev=False)

parser.add_argument('hosts', metavar='host(s)', type=str)
# parser.add_argument('-p', '--ports', metavar='port(s)', default='1-100', type=str, action='store')

args = parser.parse_args()

print("Searching for active hosts...")

scanner = nmap.PortScanner()
result = scanner.scan(args.hosts, arguments='-p80 -sS')

for item in result['scan'].keys():
    if result['scan'][item]["status"]["state"] == "up":
        print(f"{item} is up.")
