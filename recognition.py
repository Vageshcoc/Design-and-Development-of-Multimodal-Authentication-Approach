import face_recognition
import cv2
import numpy as np
import pickle
from datetime import datetime, timedelta
import winsound
unknowncounter=0
counter=0

def detectPerson():
    global unknowncounter
    global counter
    
    # Load reference data from pickle files
    with open("ref_name.pkl", "rb") as f:
        ref_dict = pickle.load(f)  # ref_dict = ref vs name

    with open("ref_embed.pkl", "rb") as f:
        embed_dict = pickle.load(f)  # embed_dict- ref vs embedding

    # Initialize arrays for known face encodings and names
    known_face_encodings = []
    known_face_names = []

    # Populate known_face_encodings and known_face_names
    for ref_id, embed_list in embed_dict.items():
        for embed in embed_list:
            known_face_encodings.append(embed)
            known_face_names.append(ref_id)

    # Initialize video capture from the default camera
    video_capture = cv2.VideoCapture(0)

    # Main loop for face recognition
    while True:
        # Capture a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color to RGB color (required by face_recognition)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Initialize list to store names of recognized faces
        face_names = []
        name=""
        # Iterate through each face in the frame
        for face_encoding in face_encodings:
            # Compare the face encoding with known face encodings
            if known_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Find the best match for the face
                if matches:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
            
                face_names.append(name)
            else:
                face_names.append("Unknown")  # No known face encodings available

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        
        # Process detected faces
        if name!="Unknown" or name!="":
            unknowncounter+=0
            counter+=1
            if counter==15:
                video_capture.release()
                cv2.destroyAllWindows()
                print(name)
                return name
        elif name=="Unknown" or name=="":
            counter+=0
            unknowncounter+=1
            if unknowncounter==15:
                video_capture.release()
                cv2.destroyAllWindows()
                return "failed"
                
        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture
    video_capture.release()
    cv2.destroyAllWindows()

# Call the function to start the detection process
#res =detectPerson()

