from keras.models import load_model
import sys

model_name = sys.argv[1]
model = load_model(model_name)
model.save_weights('DeepCSV_weights.h5')


from models import dense_model
from DeepJetCore.training.training_base import training_base

from keras.layers import Dense, Dropout, Flatten, Convolution2D, merge, Convolution1D, Conv2D
from keras.models import Model, Sequential

nclasses = 4

model = Sequential( [

     Dense(100, activation='relu',kernel_initializer='lecun_uniform', input_shape=(66,1)),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(nclasses, activation='softmax',kernel_initializer='lecun_uniform')
])

arch = model.to_json()
with open('DeepCSV_arch.json', 'w') as arch_file:
    arch_file.write(arch)
