import sys

def main():
    out = []
    for line in sys.stdin.buffer:
        nums = [int(x) for x in line.split()]
        out.append(str(sum(nums)))
    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()
