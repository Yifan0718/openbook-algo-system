import sys
from collections import Counter

def main():
    tokens = sys.stdin.buffer.read().decode().split()
    if not tokens:
        return
    k = int(tokens[0])
    words = tokens[1:]
    cnt = Counter(words)
    order = sorted(cnt.items(), key=lambda item: (-item[1], item[0]))
    for word, times in order[:k]:
        print(word, times)

if __name__ == "__main__":
    main()
