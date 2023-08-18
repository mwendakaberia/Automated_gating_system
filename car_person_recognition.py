import tensorflow as tf
import keras
import numpy as np

model=keras.models.load_model('car_person_model.h5')

height=180
width=180

class_names=['cars', 'people']

#path='C:/Users/MeanRegression/Desktop/dataset/images/Cars27.png'
import GUI
path=GUI.loc
img=keras.preprocessing.image.load_img(path,target_size=(height,width))
img=keras.preprocessing.image.img_to_array(img)
img=tf.expand_dims(img,0)
#print(img.shape)
predictions=model.predict(img)
score=tf.nn.softmax(predictions[0])
name=class_names[np.argmax(score)]
# print("This image most likely belongs to  {}  with a  {:.2f}  percent confidence.".format(
#      name,100*np.max(score)))

if(name=="cars"):
     import plate_recognition
    # GUI.label1.config(text=plate_recognition.text)
else:
     import face_recognition
     #GUI.label1.config(text=face_recognition.score)
