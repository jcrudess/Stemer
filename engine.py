from spleeter.separator import Separator


def stemaj(file, folder, mode):
    print("pozivam funkciju")
    separator = Separator(mode)
    separator.separate_to_file(file, folder)
