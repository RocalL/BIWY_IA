import face_recognition
import cv2
import os, glob
import simplejson
import numpy as np
import bdd_access
from datetime import datetime


video_capture = cv2.VideoCapture(0)

known_face_names = []
known_face_encodings = []

f = open('known_face_name.txt', 'r')
known_face_names = simplejson.load(f)

known_face_encodings = np.loadtxt('known_face_encodings.txt')

face_locations = []
face_encodings = []
face_names = []
concerned_faces = bdd_access.bdd_get_p_from_cp(1)
update_time = {}
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
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                face_id = name.split("_")[0]
                face_name = name.split("_")[1]
                if int(face_id) in concerned_faces:
                    try:
                        update_time[face_id]
                    except:
                        update_time[face_id] = datetime.now()
                    #print(face_name + " : present")

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
        bdd_access.bdd_insert_presence(update_time,1)
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
