import face_recognition  #Python Library for Face Recognition System
import cv2 #OpenCV Library for Facial Recognition using Real time web data.
import os
import subprocess
from Crypto import Random #for SSL Encryption
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time

###################################DEFINING ENCRYPTION CLASSES AND FUNCTIONS######################################

class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
clear = lambda: os.system('cls')

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
yourface_image = face_recognition.load_image_file("obama.jpg")
your_face_encoding = face_recognition.face_encodings(yourface_image,num_jitters=100)[0]

# Load a second sample picture and learn how to recognize it.
yoursecondface_image = face_recognition.load_image_file("obama.jpg")
yoursecondface_face_encoding = face_recognition.face_encodings(yoursecondface_image,num_jitters=100)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    your_face_encoding,
    yoursecondface_face_encoding
]
known_face_names = [
    "Atul",
    "Atul"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
            name = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                os.system("say -v Daniel Welcome Sir all files are ready for encryption process.")
                if os.path.isfile('data.txt.enc'):
                    while True:
                        password = str(input("Enter 2 Step Verification:"))
                        enc.decrypt_file("data.txt.enc")
                        p = ''
                        with open("data.txt", "r") as f:
                            p = f.readlines()
                        if p[0] == password:
                            enc.encrypt_file("data.txt")
                            break
                        else:
                            print("Wrong Password Please Try Again")
                            enc.encrypt_file("data.txt")

                    while True:
                        clear()
                        choice = int(input(
                            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the "
                            "directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
                        clear()
                        if choice == 1:
                            enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
                        elif choice == 2:
                            enc.decrypt_file(str(input("Enter name of file to decrypt: ")))
                        elif choice == 3:
                            enc.encrypt_all_files()
                        elif choice == 4:
                            enc.decrypt_all_files()
                        elif choice == 5:
                            exit()
                        else:
                            print("Please select a valid option!")

                else:
                    while True:
                        clear()
                        password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
                        repassword = str(input("Confirm password: "))
                        if password == repassword:
                            break
                        else:
                            print("Passwords Mismatched!")
                    f = open("data.txt", "w+")
                    f.write(password)
                    f.close()
                    enc.encrypt_file("data.txt")
                    print("Please restart the program to complete the setup")
                    time.sleep(15)
                ##if name == 'Atul':
               ##     os.system("say -v Daniel Welcome it's you wow!, Good to see you again")
             ##   print("Face Detected Opening the Two-Step Verification System")
            ##    exec(open('script.py').read())
            else:
                os.system("say -v Daniel Sorry but you are not authorised to access the files.")

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


#This code is written/modified by Atul.
