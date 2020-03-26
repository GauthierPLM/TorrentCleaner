from pathlib import Path

from typing import List


class CLI:
    def display_file_list(self, not_in_paths: List[Path]):
        for file in not_in_paths:
            print(file)

    def ask_file_delete(self) -> bool:
        should_delete_files = input("Do you want to delete the files not included in the torrent?")
        return should_delete_files.lower() == "y"
