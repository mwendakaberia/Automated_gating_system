import keras
import tensorflow as tf
import numpy as np

from car_person_recognition import path

height=180
width=180

class_names=['Large', 'Red', 'Roma']

model=keras.models.load_model('face_model.h5')

#path='C:/Users/MeanRegression/Desktop/ndackia/note 7/IMG_20201225_161332_302.jpg'
img=keras.preprocessing.image.load_img(path,target_size=(height,width))
img=keras.preprocessing.image.img_to_array(img)
img=tf.expand_dims(img,0)
print(img.shape)

predictions=model.predict(img)
score=tf.nn.softmax(predictions[0])


print("This image most likely belongs to  {}  with a  {:.2f}  percent confidence."
      .format(class_names[np.argmax(score)],100*np.max(score)))
