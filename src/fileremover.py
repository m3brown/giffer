from os import remove


def remove_file(filepath):
    print("Deleting %s" % filepath)
    remove(filepath)
