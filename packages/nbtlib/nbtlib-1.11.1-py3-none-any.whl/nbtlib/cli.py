from json import dumps as json_dumps
from pprint import pprint
from argparse import ArgumentParser, ArgumentTypeError


from nbtlib import nbt, parse_nbt, serialize_tag, InvalidLiteral, Path
from nbtlib.tag import Compound, find_tag


# Validation helper


def nbt_data(literal):
    try:
        nbt_data = parse_nbt(literal)
    except InvalidLiteral as exc:
        raise ArgumentTypeError(exc) from exc
    else:
        if not isinstance(nbt_data, Compound):
            raise ArgumentTypeError("The root nbt tag must be a compound tag")
        return nbt_data


# Create the argument parser

parser = ArgumentParser(prog="nbt", description="Perform operations on nbt files.")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-r", action="store_true", help="read nbt data from a file")
group.add_argument("-s", action="store_true", help="read snbt from a file")
group.add_argument("-w", metavar="<nbt>", type=nbt_data, help="write nbt to a file")
group.add_argument("-m", metavar="<nbt>", type=nbt_data, help="merge nbt into a file")

parser.add_argument("--plain", action="store_true", help="don't use gzip compression")
parser.add_argument("--little", action="store_true", help="use little-endian format")

parser.add_argument("--compact", action="store_true", help="output compact snbt")
parser.add_argument("--pretty", action="store_true", help="output indented snbt")
parser.add_argument("--unpack", action="store_true", help="output interpreted nbt")
parser.add_argument("--json", action="store_true", help="output nbt as json")
parser.add_argument("--path", metavar="<path>", help="output all the matching tags")
parser.add_argument(
    "--find", metavar="<path>", help="recursively find the first matching tag"
)

parser.add_argument("file", metavar="<file>", help="the target file")


# Define command-line interface


def main():
    args = parser.parse_args()
    gzipped, byteorder = not args.plain, "little" if args.little else "big"
    try:
        if args.r or args.s:
            read(
                args.file,
                gzipped,
                byteorder,
                args.s,
                args.compact,
                args.pretty,
                args.unpack,
                args.json,
                args.path,
                args.find,
            )
        elif args.w:
            write(args.w, args.file, gzipped, byteorder)
        elif args.m:
            merge(args.m, args.file, gzipped, byteorder)
    except IOError as exc:
        parser.exit(1, str(exc) + "\n")


def read(filename, gzipped, byteorder, snbt, compact, pretty, unpack, json, path, find):
    if snbt:
        with open(filename) as f:
            nbt_file = parse_nbt(f.read())
    else:
        nbt_file = nbt.load(filename, gzipped=gzipped, byteorder=byteorder)

    tags = nbt_file.get_all(Path(path)) if path else [nbt_file]

    for tag in tags:
        if find:
            tag = find_tag(Path(find), [tag])
        if tag is None:
            continue
        if unpack:
            if pretty:
                pprint(tag.unpack())
            else:
                print(tag.unpack())
        elif json:
            print(json_dumps(tag.unpack(json=True), indent=4 if pretty else None))
        else:
            print(serialize_tag(tag, indent=4 if pretty else None, compact=compact))


def write(nbt_data, filename, gzipped, byteorder):
    nbt.File(nbt_data).save(filename, gzipped=gzipped, byteorder=byteorder)


def merge(nbt_data, filename, gzipped, byteorder):
    nbt_file = nbt.load(filename, gzipped=gzipped, byteorder=byteorder)
    nbt_file.merge(nbt_data)
    nbt_file.save()
