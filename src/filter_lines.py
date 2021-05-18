import random
import argparse


def main(infile, outfile, count):
  x = open(infile).readlines()
  y = random.sample(x, count)
  open(outfile, "w").write("".join(y))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--infile", required=True)
  parser.add_argument("--outfile", required=True)
  parser.add_argument("--count", type=int, required=True)
  main(**parser.parse_args().__dict__)
