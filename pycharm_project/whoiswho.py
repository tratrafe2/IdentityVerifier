from WIW_lib import *
import sys


def exit_error(message, code):
    """
    Responsible for printing the correct error message and exiting the program.
    :param message: The message to be printed as a reference for the user
    :param code: The code that the exit function of python will use to exit the application.
    :return:  no return
    """
    print(message)
    exit(code)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        exit_error("Wrong number of arguments", 5)

    imagepath = sys.argv[1]
    docdir = sys.argv[2]

    if not os.path.isfile(imagepath):
        exit_error("Sampling file does not exist.", 1)

    if not os.path.isdir(docdir):
        exit_error("Document directory does not exist.", 2)

    sample = scan_file(imagepath)
    if sample is None:
        exit_error("Could not detect a front face on sampling image.", 3)

    docs = scan_path(docdir)
    if len(docs) < 1:
        exit_error("Could not detect any front faces on the document's folder.", 4)

    result = compare_image(docs, sample, 0.5)
    if result is not None:
        print('{} matched {} in {}.'.format(imagepath, result['name'], docdir))
    else:
        print("{} not matched {}.".format(imagepath, docdir))