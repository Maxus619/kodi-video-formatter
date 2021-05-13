import os
from pathlib import Path


print('Input TV Show name:')
tv_name = input()
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), tv_name)

# Exceptions
if not tv_name:
    print("Name is empty")
    exit()
elif not os.path.exists(path):
    print("TV Show folder is not found")
    exit()

subs_ext = ['.ass', '.srt', '.ttf']
special_folders = ['Special', 'Specials', 'SP']
episode = 1


def tv_file_format(file, _season, _episode):
    name, _ext = os.path.splitext(file)
    new_name = os.path.join(str(Path(file).parents[0]),
                            tv_name + ' - S' + str(_season).zfill(2) + 'E' + str(_episode).zfill(2) + _ext)
    os.rename(file, new_name)


def subs_format(_path, _season=None):
    _episode = 1
    for sub_name in os.listdir(_path):
        _, _ext = os.path.splitext(sub_name)
        if _ext:
            full_sub_name = os.path.join(_path, sub_name)
            tv_file_format(full_sub_name, _season if _season else 1, _episode)
            _episode += 1


def specials_format(_path):
    _episode = 1
    for special_name in os.listdir(_path):
        full_special_name = os.path.join(_path, special_name)
        tv_file_format(full_special_name, 0, _episode)
        _episode += 1


# Checking "Season" folders
if 'Season' in os.listdir(path)[0]:
    for season_file_name in os.listdir(path):
        season = season_file_name.split()[-1]
        path = os.path.join(path, season_file_name)

        for file_name in os.listdir(path):
            _, ext = os.path.splitext(file_name)

            # Moving subtitles in "Subs" folder
            if ext in subs_ext:
                if not os.path.exists(path + "\\Subs"):
                    os.makedirs(path + "\\Subs")

                os.rename(path + "\\" + file_name,
                          path + "\\Subs\\" + file_name)

            # Specials formatting
            elif file_name in special_folders:
                special_folder = path + "\\" + file_name
                specials_format(special_folder)

            # Videos formatting
            else:
                if ext:
                    full_file_name = os.path.join(path, file_name)
                    tv_file_format(full_file_name, season, episode)
                    episode += 1

        # Subs formatting
        subs_path = path + "\\Subs"
        if os.path.exists(subs_path):
            subs_format(subs_path, season)

        path = str(Path(path).parents[0])
        episode = 1
else:
    for file_name in os.listdir(path):
        _, ext = os.path.splitext(file_name)

        if ext in subs_ext:
            if not os.path.exists(path + "\\Subs"):
                os.makedirs(path + "\\Subs")

            os.rename(path + "\\" + file_name,
                      path + "\\Subs\\" + file_name)

        elif file_name in special_folders:
            special_folder = path + "\\" + file_name
            specials_format(special_folder)

        else:
            if ext:
                full_file_name = os.path.join(path, file_name)
                tv_file_format(full_file_name, 1, episode)
                episode += 1

    subs_path = path + "\\Subs"
    if os.path.exists(subs_path):
        subs_format(subs_path)

print("Done!")
