from keras import backend
from keras.models import Sequential, load_model
from keras.layers import Dense
import numpy as np

backend.set_learning_phase(0)

class Model():
    def __init__(self, identifier, input_size):

        if identifier != -1:
            self.model = load_model("models/"+str(identifier)+".h5")

        else:
            self.model = Sequential()
            self.model.add(Dense(input_size))
            self.model.add(Dense(20 , kernel_initializer="random_uniform",
                                    bias_initializer="random_uniform",
                                    activation="relu"))
            self.model.add(Dense(20, kernel_initializer="random_uniform",
                                    bias_initializer="random_uniform",
                                    activation="relu"))
            self.model.add(Dense(4, activation="linear"))

            self.model.compile(loss='binary_crossentropy', optimizer="adam")      
        
    def frame(self, input_data): #input_data is a list of the 16 inputs
        input_data = [np.array([input_data])]
        
        output_data = self.model.predict(input_data)
        output_data = output_data.flatten().tolist()
        out = []

        for val in output_data:
            if val > 0.6:
                val = 1
            elif val < 0.4:
                val = 0
            else:
                val = 0.5
            out.append(val)
            
        return out


    def evolve(self, other):
        models = [self.model, other.model]
        weights = [model.get_weights() for model in models]
        new_weights = list()

        for weights_list_tuple in zip(*weights):
            new_weights.append([np.array(weights_).mean(axis=0)
                                for weights_ in zip(*weights_list_tuple)])

        self.model.set_weights(new_weights)


    def save(self,identifier):
        self.model.save("models/"+str(identifier)+".h5")
        del self.model


def clear():
    backend.clear_session()
