import os
import sys
from os import walk
from pathlib import Path
from shutil import copyfile

def do(argv):
    # print(argv)
    # print(os.path.abspath(os.curdir))

    def git_psh(dest_path):
        os.system(f'cd {dest_path} && git pull && git add . && git commit -am"." && git push')

    max_size = 1024 * 1024 * 1024

    if len(argv) < 2 or not os.path.isdir(argv[1]):
        raise Exception('The path must contain the source directory')

    if len(argv) < 3 or not os.path.isdir(argv[2]):
        raise Exception('The path must contain the destination directory')

    source_path = argv[1]
    dest_path = argv[2]
    excl = ['.git', '.idea']

    files = []
    for (dirpath, dirnames, filenames) in walk(source_path):
        for filename in filenames:
            full_path_source = f'{dirpath}{os.sep}{filename}'
            exclude = len(list(filter(lambda x: dirpath.find(x) != -1, excl))) > 0
            if exclude is True:
                continue
            stat_source = Path(full_path_source).stat()

            full_path_dest = full_path_source.replace(source_path, dest_path)
            dir_path_dest = dirpath.replace(source_path, dest_path)
            if not os.path.exists(full_path_dest):
                files.append((full_path_source, dir_path_dest, full_path_dest, stat_source.st_size))
            else:
                stat_dest = Path(full_path_dest).stat()
                # if stat_source.st_size != stat_dest.st_size or stat_source.st_mtime != stat_dest.st_mtime:
                if stat_source.st_size != stat_dest.st_size:
                    files.append((full_path_source, dir_path_dest, full_path_dest, stat_source.st_size))

    sized = 0
    for src, dir_dst, dst, size in files:
        if sized + size > max_size:
            if sized > 0:
                git_psh(dest_path=dest_path)
            return False

        if not os.path.exists(dir_dst):
            os.makedirs(dir_dst)

        copyfile(src, dst)
        print(f'Copied {src} -> {dst}')
        sized += size

    if sized > 0:
        git_psh(dest_path=dest_path)

    return True


if __name__ == '__main__':
    a = False
    while a is False:
        a = do(sys.argv)
