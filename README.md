# MyStyle

MyStyle is a program that learns what you like in your pictures. 
Simply add images that you relatively like in the pos folder,
images that relatively do not like in the neg folder, and images 
you want to test in the test folder. Run the flask app and 
navigate to localhost on the port provided. 

The program then extracts features from your images ranging from 
content to color, and then uses Microsoft Azure to run a neural network
to classify the test images. Kinda. This project is in pieces for 
various reasons. There is an Azure Machine Learning Experiment that 
takes training data you specified to create a model. And you can interact
with the web service created from this experimented. You just have to hop
around. 

### Future Work

Obviously one thing we want to do is completely implement MyStyle from 
start to finish in one place. Currently the web interface does not work,
and we want to move to a regression model of sorts to give rankings of images.
