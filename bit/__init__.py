from bit.core.workspace import Workspace
from bit.core.utility import pushd, flatten
from bit.core.color import error

import os

def main():
    with Workspace() as bit:
        directory = bit.args.directory
        os.makedirs(bit.cache, exist_ok=True)
        with pushd(directory):
            bit.load(os.path.join(directory, bit.args.file))
            if bit.args.show_options: bit.parser.print_help()
            bit.run()
