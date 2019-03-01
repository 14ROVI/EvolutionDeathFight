from keras import backend
from keras.models import Sequential, load_model
from keras.layers import Dense
import numpy as np
import random

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

    def mutate(self):

        # first itterate through the layers
        for j, layer in enumerate(self.model.layers):
            new_weights_for_layer = []
            # each layer has 2 matrizes, one for connection weights and one for biases
            # then itterate though each matrix

            for weight_array in layer.get_weights():
                # save their shape
                save_shape = weight_array.shape
                # reshape them to one dimension
                one_dim_weight = weight_array.reshape(-1)

                for i, weight in enumerate(one_dim_weight):
                    # mutate them like i want
                    if random.uniform(0, 1) <= 0.1:
                        # maybe dont use a complete new weigh, but rather just change it a bit
                        one_dim_weight[i] *= np.random.normal(mean=1,std=0.05)

                # reshape them back to the original form
                new_weight_array = one_dim_weight.reshape(save_shape)
                # save them to the weight list for the layer
                new_weights_for_layer.append(new_weight_array)

            # set the new weight list for each layer
            self.model.layers[j].set_weights(new_weights_for_layer)



    def save(self,identifier):
        self.model.save("models/"+str(identifier)+".h5")
        del self.model


def clear():
    backend.clear_session()
