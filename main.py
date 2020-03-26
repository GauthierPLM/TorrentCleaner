from pathlib import Path

import argparse
import torrent_parser as tp
from typing import List

from CLI import CLI


class Main:
    paths = []

    def parse_args(self):
        parser = argparse.ArgumentParser(description="This program list files in the specified directory that are not "
                                                     "part of the specified torrent.")
        parser.add_argument("torrent", help="Torrent file path")
        parser.add_argument("path", nargs='?', default=Path.cwd(), help="Path to check")
        parser.add_argument("-d", "--dry-run", help="Do not change anything", action="store_true")
        args = parser.parse_args()

        return args

    def __init__(self):
        view = CLI()

        args = self.parse_args()
        base_path = Path(args.path)
        data = tp.parse_torrent_file(args.torrent)

        for file in data["info"]["files"]:
            self.paths.append(Path(base_path, *file["path"]))

        not_in_path = self.check_dir(base_path)

        print("Files not in path: ", len(not_in_path))
        if len(not_in_path) != 0:
            print("Files:")
            view.display_file_list(not_in_path)

            if not args.dry_run and view.ask_file_delete():
                self.delete_files(not_in_path)

    def delete_files(self, not_in_paths: List[Path]):
        for file in not_in_paths:
            if file.is_file():
                file.rmdir()

    def check_dir(self, cwd: Path) -> List[Path]:
        not_in_path = []

        for file in cwd.iterdir():
            if file.is_dir():
                not_in_path += self.check_dir(file)
            elif file not in self.paths:
                not_in_path.append(file)

        return not_in_path


if __name__ == '__main__':
    Main()
