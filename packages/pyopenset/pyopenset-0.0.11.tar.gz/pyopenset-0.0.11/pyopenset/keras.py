#Dependences for layer
from keras.constraints import min_max_norm
from keras.layers import Layer
import tensorflow as tf
import keras.backend as K
import keras

#Layer that takes a input and normalizes it to norm s, use it just before the dense layer
class ModuleNormalization(Layer):
    def __init__(self,s=10,**kwargs):
        super(ModuleNormalization, self).__init__()
        #w_init = K.random_normal_initializer()
        self.w = tf.Variable(
            initial_value=s,
            trainable=False,
        ).numpy()
        
    def call(self, inputs):
      #x/K.sqrt(K.sum((x)**2))
       # inputs=inputs/K.sqrt(K.sum(inputs**2) )
        inputs=K.l2_normalize(inputs,axis=-1)       
        return (inputs)*K.abs(self.w)   #tf.matmul(inputs, self.w) #+ self.b 



    def get_config(self):
        config = super().get_config().copy()
        config.update({
            's': self.w           
        })
        return config


    def build(self, input_shape):
        output_dim = input_shape#[-1]
        #self.kernel = self.add_weight(
         #   shape=(output_dim),
            #initializer=self.initializer,
          #  name="kernel",
           # trainable=True,
        #)





#Function that takes as a input a keras model with k neurons and a softmax activation function on the last layer and returns the same model with 1 extra neuron corresponding to the class belonging to X
#Arguments model1: A keras model
	   #X a numpy array containing the new class examples to be fed into the
def AddNewClass(model1,X):
  import numpy as np
  from keras.models import Model
  from keras.layers import Dense
  Weights=model1.layers[-1].get_weights()
  ClassWeights=Weights[0]
  model=Model(model1.input,model1.layers[-2].output)
  Embeddings=model.predict(X)
  ProtValue=np.mean(Embeddings,axis=0)
  ProtValue=ProtValue/np.sqrt(np.sum(ProtValue**2) )
  #print(ClassWeights.shape)
  NewWeights=np.zeros(shape=(ClassWeights.shape[0],ClassWeights.shape[1]+1))
  NewWeights[:,0:(ClassWeights.shape[1]) ]=ClassWeights
  NewWeights[:,NewWeights.shape[1]-1]=ProtValue
  Neurons=ClassWeights.shape[1]+1
  x=Dense(Neurons,kernel_constraint=min_max_norm(1,1),bias_constraint=min_max_norm(0,0),activation='softmax')(model.layers[-1].output)
  NewModel=Model(model.input,x)
  WeightsPlusBiases=NewModel.layers[-1].get_weights()
  WeightsPlusBiases[0]=NewWeights
  NewModel.layers[-1].set_weights(WeightsPlusBiases)
  return(NewModel)

def CreateNewModel(model1,X): #Disjoint scenario. You create the new model with this function and then run AddNewClass for other classes
  import numpy as np
  from keras.models import Model
  from keras.layers import Dense
  Weights=model1.layers[-1].get_weights()
  ClassWeights=Weights[0]
  model=Model(model1.input,model1.layers[-2].output)
  Embeddings=model.predict(X)
  ProtValue=np.mean(Embeddings,axis=0)
  ProtValue=ProtValue/np.sqrt(np.sum(ProtValue**2) )
  #print(ClassWeights.shape)
  NewWeights=np.zeros(shape=(ClassWeights.shape[0],1))
  #NewWeights[:,0:(ClassWeights.shape[1]) ]=ClassWeights
  NewWeights[:,NewWeights.shape[1]-1]=ProtValue
  Neurons=ClassWeights.shape[1]+1
  x=Dense(1,kernel_constraint=min_max_norm(1,1),bias_constraint=min_max_norm(0,0),activation='softmax')(model.layers[-1].output)
  NewModel=Model(model.input,x)
  WeightsPlusBiases=NewModel.layers[-1].get_weights()
  WeightsPlusBiases[0]=NewWeights
  NewModel.layers[-1].set_weights(WeightsPlusBiases)
  return(NewModel)



