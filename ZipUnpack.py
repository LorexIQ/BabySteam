import zipfile
import time

zip_progress = 0
zip_info = [0, 0]

def delay_pecent(a, b):
    global zip_progress
    if int(a) != int(b):
        if int(b) - int(a) > 20:
            for face_percent in range(int(a), int(b) + 1):
                zip_progress = face_percent
                time.sleep(int(b - a) / 5000)
        else:
            zip_progress = b

def unzip():
    global zip_info
    zip_info = [0, 0]
    new_progress = 0
    zip_unpack = zipfile.ZipFile('babysteamapps/file.zip')
    files = zip_unpack.namelist()
    deleting_folders = []
    for count_file in range(len(files)):
        if files[count_file][-1] == '/':
            deleting_folders.append(files[count_file])
    for deliting_line in deleting_folders:
        files.pop(files.index(deliting_line))
    zip_info[1] = len(files)
    for file in files:
        old_progress = new_progress
        new_progress = round((files.index(file) + 1) * 100 / len(files), 1)
        zip_unpack.extract(file, 'babysteamapps')
        delay_pecent(old_progress, new_progress)
        zip_info[0] += 1
