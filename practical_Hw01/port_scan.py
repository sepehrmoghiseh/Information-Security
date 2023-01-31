import nmap
import argparse


parser = argparse.ArgumentParser(prog="my-port-scan", allow_abbrev=False)

parser.add_argument('hosts', metavar='host(s)', type=str)
parser.add_argument('-p', '--ports', metavar='port(s)', default='1-1023', type=str, action='store')

args = parser.parse_args()

print("Searching...")

scanner = nmap.PortScanner()
result = scanner.scan(args.hosts, args.ports, arguments='-sS')

for host in result['scan']:
    for port in result['scan'][host].get("tcp", {}):
        if result['scan'][host]["tcp"][port]["state"] == "open":
            print(f"{host}:{port} is open.")
