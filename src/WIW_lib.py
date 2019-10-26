import face_recognition.api as face_recognition
import numpy
import cv2
import os
import pickle
import base64
import time


def get_face(imagePath):
    """
    This function reads an image from a given path and by using the opencv library, and a given cascade xml file,
    it detects all faces in the image and returns a cropped image containing only the dominant face.
    :param imagePath: The path to the image
    :return: Returns a cropped image containing the dominant face.
             If a face is not recognised a none object returns.
    """
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces) < 1:
        return None
    (x, y, w, h) = faces[0]
    crop_img = image[y:y + h, x:x + w]
    return crop_img


def scan_file(path):
    """
    This function reads an image from a given path.
    Afterwards it uses the function getface() to locate the face in the image, and finally extracts the facial
    characteristics from the face part of the image by using the face_recognition api.

    :param path: The path of the image we want to extract the characteristics from.
    :return: Returns an object with all the characteristics of the image.
             If a face is not recognised or has no characteristics, a none object is returned.
    """
    image = get_face(path)
    if image is not None:
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            img = {
                'image': image,
                'encodings': encodings[0],
                'name': path
            }
            return img

    return None


def scan_path(directory):
    """
    This function reads image files from a given directory.
    Afterwards it uses the function get_face() to locate the face in the image, and finally extracts the facial
    characteristics from the face part of the image by using the face_recognition api.
    The extracted characteristics are saved as a pickle file in another directory. This allows to save time by
    skipping the calculation of known directories. In case the modification date of a directory has changed,
    the characteristics are recalculated.

    :param directory: The path to the images we want to extract the characteristics from.
    :return: Returns an object with all the characteristics for every image in the directory if they exists.
             Otherwise an empty array will be returned.
    """
    objname= str(base64.b64encode(directory.encode('utf-8')))
    preprocess='preprocess'

    if not os.path.isdir(preprocess):
        os.mkdir(preprocess)
    if os.path.isfile(preprocess+'/'+objname):
        picklefile=open(preprocess+'/'+objname,'rb')
        obj=pickle.load(picklefile)
        if time.ctime(os.path.getmtime(directory))==obj['lastmodified']:
            return obj['images']

    images=[]
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:
            path=dirpath+'/'+f;
            image=get_face(path)
            if image is not None:
                encodings = face_recognition.face_encodings(image)
                if len(encodings) > 0:
                    img = {
                        'image': image,
                        'encodings': encodings,
                        'name': f
                    }
                    images.append(img)

    obj={
        'lastmodified':time.ctime(os.path.getmtime(directory)),
        'images': images
    }
    file=open(preprocess+'/'+objname,'wb')
    pickle.dump(obj,file)

    return images


def compare_image(documents, sample, e):
    """
    This function compares a single image against a list of other images and returns the image
    with the best similarity value that is below a certain error value.
    The similarity value is calculated by a linear algebra normalization of the difference between the encodings of 2
    faces.
    :param documents: The list of the images that will be compared against the single image.
    :param sample: The single image
    :param e: The constant error value
    :return: The image with the best similarity value
    """
    sampleEncodings=sample['encodings']
    min= e
    best=None
    for d in documents:
        docEncodings=d['encodings'];
        x=numpy.linalg.norm(docEncodings - sampleEncodings, axis=1)
        if x< min:
            min=x
            best=d
    if min<= e:
        return best
    return None
