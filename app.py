import glob
import shutil
import subprocess
import os


class File:
    def __init__(self,
                 path):
        self.metadata = {}
        exifToolPath = 'exifTool.exe'
        ''' use Exif tool to get the metadata '''
        process = subprocess.Popen(
            [
                exifToolPath,
                path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        ''' get the tags in dict '''
        for tag in process.stdout:
            tag = tag.strip()
            key = tag[:tag.find(':')].strip()
            value = tag[tag.find(':') + 1:].strip()
            self.metadata[key] = value

    def _get_time(self):
        if 'Date/Time Original' in self.metadata:
            return self.metadata['Date/Time Original']
        elif 'Create Date' in self.metadata:
            return self.metadata['Create Date']
        else:
            return ''

    def _get_type(self):
        if 'MIME Type' in self.metadata:
            return self.metadata['MIME Type']
        else:
            return ''

    def _copyFile(self, dst: str):

        date = File._get_time(self)
        if not date:
            return False

        mime_type = File._get_type(self)
        if not mime_type:
            return False

        dst += '/' + mime_type[:mime_type.find('/')] + '/' + date[:4] + '/' + date[5:7]

        if not os.path.isdir(dst):
            os.makedirs(dst)
            print(f"Make dir {dst}")

        filename = self.metadata['File Name']
        dst_name = dst + '/' + filename
        pth: str = self.metadata['Directory'] + '/' + filename
        i = 0
        f_name = filename

        while os.path.isfile(dst_name):
            filename = f_name[:f_name.find('.')] + '_D' + str(i) + '.' + self.metadata['File Type Extension']
            dst_name = dst + '/' + filename
            i = i + 1

        if i != 0:
            print(f"Warning: {pth} -> {dst_name}")
        shutil.copy(pth, dst_name)
        print(f"{pth} -> {dst_name} Copy done ...")
        return True


def main():
    root_dir = 'C:/Users/'
    dst_dir = 'C:/Users/'
    dst_none = dst_dir + '/none'

    if not os.path.isdir(dst_none):
        os.makedirs(dst_none)
        print(f"Make dir {dst_none}")

    for p in glob.glob(root_dir + '/**/*.*', recursive=True):
        try:
            f = File(p)
            if not f._copyFile(dst_dir):
                # Exiftool { Error: No found file }
                # Path for Windows
                filename = p[p.rfind('\\'):]
                f_name = filename
                dst_none_name = dst_none + '/' + f_name
                i = 0

                while os.path.isfile(dst_none_name):
                    filename = f_name[:f_name.rfind('.')] + '_D' + str(i) + f_name[f_name.rfind('.'):]
                    dst_none_name = dst_none + '/' + filename
                    i = i + 1

                if i != 0:
                    print(f"Warning: {p} -> {dst_none_name}")

                shutil.copy(p, dst_none_name)
                print(f"{p} -> {dst_none_name} Copy done ...")
        except:
            print(f'Copy error: {p}')


if __name__ == '__main__':
    main()
