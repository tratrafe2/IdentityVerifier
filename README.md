# IdentityVerifier

## Introduction

> A face recognition application matching an unknown face with a list of known faces. The program takes as parameters the path to an image file containing a "selfie" image and a path to a directory containing document images and tries to identify the person.

## How it works

> The application uses a combination of open source libraries and mathematical equations to
calculate the differences between the faces in the images given.
At the beginning, an algorithm locates the faces in the images and exports the
characteristics of each face. Then, it creates an object table for the characteristics of each
face. Afterwards the characteristics of the given sample are calculated. Finally, the distance between the sample image and all the images in the directory folder are computed. The image with the smallest distance from the directory is the most likely to contain the person of the sample image.
An error constant restricts the false positive answer if a person is not contained in the directory file.

## Run the application

>To run the application use `python3 whoiswho.py <sample_image> <document_directory>` in the directory `pycharm_project`.

## Optimization

> In order to perform faster, the application creates an object file in the current directory
where the application is launched.
This object file contains the characteristics information about the directory file and the images contained in it. This is recreated every time a change in the directory file is monitored.

## Installation
### For Linux
>1. Download the zip folder of the git repository containing the code of the application.
2. In the directory `src` run the command `python3 -m pip install -r requirements.txt` in order to obtain all the libraries to launch the application.
3. Launch the application using `python3 whoiswho.py <sample_image> <document_directory>` in the directory `src`.
