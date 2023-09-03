import cv2
import face_recognition
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import numpy as np

class FaceRecognitionApp:
    def __init__(self, root, known_faces_dir):
        self.root = root
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings, self.known_face_names = self.load_known_faces()

        self.video_capture = cv2.VideoCapture(0)
        self.face_image_label = ttk.Label(root)
        self.face_image_label.pack()

        self.recognize_face()

    def load_known_faces(self):
        known_face_encodings = []
        known_face_names = []
        for file_name in os.listdir(self.known_faces_dir):
            image_path = os.path.join(self.known_faces_dir, file_name)
            known_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(known_image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(file_name)[0])
        return known_face_encodings, known_face_names

    def recognize_face(self):
        ret, frame = self.video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left * 4 + 6, bottom * 4 - 6), font, 0.5, (255, 255, 255), 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image)

        self.face_image_label.config(image=image_tk)
        self.face_image_label.image = image_tk

        self.root.after(10, self.recognize_face)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Face Recognition App")
    known_faces_directory = './db/'  # Replace this with the path to the directory containing known faces
    app = FaceRecognitionApp(root, known_faces_directory)
    app.run()