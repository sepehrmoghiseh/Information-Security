import argparse
import ping3
ping3.EXCEPTIONS = True

parser = argparse.ArgumentParser(prog="myping", allow_abbrev=False)

parser.add_argument('host', type=str)
parser.add_argument('-n', metavar='number_of_packets', default=3, type=int, action='store')
parser.add_argument('-t', '--timeout', metavar='seconds', default=1, type=float, action='store')
parser.add_argument('-s', '--size', metavar='bytes', default=56, type=int, action='store')

args = parser.parse_args()
real_size = args.size + 8

print(f"Pinging {args.host}")
rtts = []
for i in range(args.n):
    try:
        result = ping3.ping(args.host, timeout=args.timeout, size=args.size)
        result = int(result * 1000)
        print(f"{real_size} bytes from {args.host}: time={result}ms")
        rtts.append(result)
    except ping3.errors.Timeout as e:
        print(str(e))
    except Exception as e:
        print(str(e))
        exit()

total = args.n
transmitted = len(rtts)
loss = round((total - transmitted) / total * 100, 2)

print(f"{total} packet(s) transmitted, {transmitted} received, {loss}% packet loss")
print(f"rtt min/avg/max = {min(rtts)}/{round(sum(rtts)/transmitted, 2)}/{max(rtts)} ms")
