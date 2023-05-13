import pyzstd
import os
import multiprocessing
import subprocess

class CompressedFileReaderFactory(object):
    _zstdFile = None

    def __init__(self, zstFile):
        if not os.path.isfile(zstFile):
            raise FileNotFoundError
        self._zstdFile = pyzstd.open(zstFile, mode="rt", encoding="UTF-8", errors="replace", newline='\n')

    def getReader(self):
        return self._zstdFile

    def getFileChunk(self, chunksize=100):
        current_pos = self._zstdFile.tell()
        ret = []
        errors = []
        for i in range(0, chunksize):
            e = self._zstdFile.readline()
            if self._zstdFile.tell() == current_pos:
                break
            current_pos = self._zstdFile.tell()
            if "\ufffd" in e:
                errors.append(e)
                continue
            ret.append(e.strip())
        return ret, errors
    def close(self):
        self._zstdFile.close()

def migrateChunk(files):
    cmd = ["lfs_migrate", "-y", "-R", "--non-block"]
    for i in files:
        command = cmd.copy()
        command.append(i)
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            print("Migration Failed for {}".format(i))

def doMigration(zstdFile, threads=4):
    readerFactory = CompressedFileReaderFactory(zstdFile)
    with multiprocessing.Pool(threads) as pool:
        files, errors = readerFactory.getFileChunk()
        while files:
            result = pool.apply_async(migrateChunk, files)
            files, curErrors = readerFactory.getFileChunk()
            errors.extend(curErrors)
        pool.close()
        pool.join()
    print("The following files have bad characters in them:")
    print(errors)

