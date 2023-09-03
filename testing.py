import os
from pathlib import Path
import face_recognition
import pickle
from collections import Counter
from PIL import Image, ImageDraw
# imagePath = './db/'
# imgebase =os.listdir(imagePath)
# for imagformat in imgebase:
#     img= cv2.imread(imagformat)
#     print(img.shape)
#     # print(img)
DEFAULT_ECONDINGS_PATH = Path('./output/encodings.pkl')
Path('training').mkdir(exist_ok=True)
Path('output').mkdir(exist_ok=True)
Path('validation').mkdir(exist_ok=True)
trainImg = './training/'
def encode_known_faces(model:str ='hog', encodings_location: Path=DEFAULT_ECONDINGS_PATH) -> None:
    names= []
    encodings=[]
    list_img = os.listdir(trainImg)

    for filename in list_img:
        filepath = os.path.join(trainImg, filename)
        name = os.path.splitext(filename)[0]
        # print(name)
        image = face_recognition.load_image_file(filepath)
        face_locatiions = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locatiions)
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)
        # print(names)
    name_endcoing= {'names': names, 'encodings': encodings}
    # print(name_endcoing)
    with encodings_location.open(mode='wb') as f:
        pickle.dump(name_endcoing,f)

# encode_known_faces()
def recognize_face(image_location: str, model: str = 'hog', encodings_location: Path = DEFAULT_ECONDINGS_PATH):
    encode_known_faces()
    with encodings_location.open(mode='rb') as f:
        loaded_encodings = pickle.load(f)
    print(loaded_encodings)
    input_image = face_recognition.load_image_file(image_location)
    input_face_locations = face_recognition.face_locations(input_image, model=model)
    input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)
    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = 'Unknown'
        _display_face(draw, bounding_box, name)
    del draw
    pillow_image.show()

BOUNDING_BOX_COLOR = 'blue'
TEXT_COLOR = 'white'

def _display_face(draw, bounding_box, name):
    top, right, bottom,left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox((left, bottom), name)
    draw.rectangle(((text_left,text_top),(text_right, text_bottom)), fill='blue', outline='blue',)
    draw.text((text_left, text_top), name, fill='white',)
    print(name)

def _recognize_face(unknown_encoding, loaded_encodings ):
    boolean_matches= face_recognition.compare_faces(loaded_encodings['encodings'], unknown_encoding)
    votes = Counter(name
                    for match, name in zip(boolean_matches, loaded_encodings['names'])
                    if match
                    )
    if votes:
        return votes.most_common(1)[0][0]


def validate(model:str='hog'):
    for filepath in Path('validation').rglob('*'):
        if filepath.is_fifo():
            recognize_face(image_location=str(filepath.absolute(), model=model))

recognize_face('test11.jpg')