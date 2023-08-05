"""
(Whitespace + Brainfuck) / 2 == Whitefuck

In this doc:
  s means space
  t measn tab


ss: increment (increase by one) the byte at the data pointer.
st: decrement (decrease by one) the byte at the data pointer.
ts: increment the data pointer (to point to the next cell to the right).
tt: decrement the data pointer (to point to the next cell to the left).
sss: output the byte at the data pointer.
sst: accept one byte of input, storing its value in the byte at the data pointer.
sts: if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
stt: if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.
"""

import argparse
import functools

d = {
    "  ": "+",
    " 	": "-",
    "	 ": ">",
    "		": "<",
    "   ": ".",
    "  	": ",",
    " 	 ": "[",
    " 		": "]"
}


def run(f, ip="", counter=1024):
    """
    Run Whitefuck script.

    Parameters
    ----------
    f : str
        Script to run.
    ip : str, optional
        Input, by default ""
    counter : int, optional
        Number of counters to make, by default 1024
    """

    s = ""
    # Format to brainfuck

    for l in f.split("\n"):
        g = d.get(l)
        if g:
            s += g

    # Check syntax

    bc = 0

    for c in s:
        if c == "[":
            bc += 1
        elif c == "]":
            bc -= 1
        assert bc >= 0

    assert bc == 0

    # Run script

    i = 0

    ii = 0

    cn = [0] * counter
    po = 0
    br = []

    while i < len(s):
        c = s[i]
        assert po in range(counter)

        if c == ">":
            po += 1
        elif c == "<":
            po -= 1
        elif c == "+":
            cn[po] += 1
        elif c == "-":
            cn[po] = max(cn[po] - 1, 0)
        elif c == ".":
            print(chr(cn[po]), end="")
        elif c == ",":
            cn[po] = ip[ii]
            ii += 1
        elif c == "[":
            if cn[po] == 0:
                while s[i] == "]":
                    i += 1
                i += 1
            else:
                br.append(i)
        elif c == "]":
            if cn[po] != 0:
                i = br[-1]
            else:
                br.pop(-1)
        i += 1
        # print(i, cn[po], po, c, len(br))


def make_function(f, ip="", counter=1024):
    """
    Make a callable.

    Parameters
    ----------
    f : str
        Script to run.
    ip : str, optional
        Input, by default ""
    counter : int, optional
        Number of counters to make, by default 1024

    Returns
    -------
    Callable
        Callable script.
    """
    return functools.partial(run, f, ip, counter)


def convert(f):
    """
    Convert brainfuck to whitefuck.

    Parameters
    ----------
    f : str
        Script to convert

    Returns
    -------
    str
        Converted script.
    """
    d2 = {v: k for k, v in d.items()}
    r = ""
    for c in f:
        if d2.get(c):
            r += d2.get(c) + "\n"

    return r


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=open, help='File to run')
    parser.add_argument('-m', '--mode', choices=['run', 'convert'], default="run", help="Mode. Default: run")

    g = parser.add_argument_group(title="Run")
    g.add_argument('-i', '--input', default="", help="A input.")
    g.add_argument('-c', '--counter', type=int, default=1024, help="Number of counters to make.")

    g = parser.add_argument_group(title="Convert")
    g.add_argument('-o', '--output', help="Path to export result.")
    args = parser.parse_args()

    f = args.file.read()
    args.file.close()
    if args.mode == "run":
        run(f, args.input)

    elif args.mode == "convert":
        r = convert(f)
        with open(args.output, "w") as fi:
            fi.write(r)


if __name__ == "__main__":
    main()
