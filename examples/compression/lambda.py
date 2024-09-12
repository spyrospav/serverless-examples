import datetime
import io
import os
import shutil
import uuid
import zlib

def compress(path, key):
    archive = os.path.join(path, key)
    shutil.make_archive(archive, 'zip', root_dir=path)
    archive_name = '{}.zip'.format(key)
    archive_size = os.path.getsize(os.path.join(path, archive_name))

    return archive_name, archive_size

def handler(event, context=None):
    local_path = event.get('local_path')
    folder_name = event.get('folder_name')
    archive_name, archive_size = compress(local_path, folder_name)

    return {
        "result": "{} compression in size {} finished!".format(archive_name, archive_size)
    }


if __name__ == "__main__":
    event = {
        'local_path': "./",
        'folder_name': "acmart"
    }
    print(handler(event))