import json
import pathlib
import argparse

parser = argparse.ArgumentParser(
    epilog="Example : python flags_to_db.py clang++.exe -s=src -o=build/obj -f=foo/compile_flags.txt")
parser.add_argument("command", type=str,
                    help="compile command")
parser.add_argument("-s", "--srcdir", type=str, default="src",
                    help="source file directory")
parser.add_argument("-o", "--objdir", type=str, default="build/obj",
                    help="object file directory")
parser.add_argument("-f", "--flagsfile",
                    type=argparse.FileType("r"),
                    default='compile_flags.txt',
                    help="compile option file")
args = parser.parse_args()

options = ""
f = args.flagsfile

for option in f:
    if ' ' in option:
        option = "\"" + option + "\""
    options += option.replace("\n", "") + ' '
f.close()

options += " -c -o"

current = pathlib.Path.cwd()
target_dir = pathlib.Path(pathlib.PurePath.joinpath(current, args.srcdir))
print(f"project root : {current}")
print(f"source dir : {target_dir}")
db = []
for file in target_dir.rglob(r"*"):
    if pathlib.re.search(r"^.*\.(h|hpp|c|cpp)$", file.name):
        file_path = str(file.relative_to(current)).replace("\\", "/")
        print(file_path)
        db.append({"directory": str(current).replace("\\", "/"),
                   "command": f"{args.command} {options} {args.objdir}/{file.name}.o {file_path}",
                   "file": file_path})

with open("compile_commands.json", 'w', encoding="utf-8") as compile_commands:
    json.dump(db, compile_commands, indent=4)
