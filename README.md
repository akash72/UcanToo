# UcanToo
An automated response system for questions related to Ubuntu/Linux.

UCanToo can help new Ubuntu users with their queries. This repository consists of both the frontend code and the backend models. 

For the front end, install ReactNative (https://facebook.github.io/react-native/) and the necessary libraries go to the folder UI and run `react-native run-ios` or `react-native run-android` depending on the platform in which you want to run to code.

To start the backend services, initially go to Modules folder and run `python Controller.py`, then navigate to MLModelInterface folder and run `python MLController.py`. To run these two controllers, all the required python libraries must have been installed. 

All of the UI code can be found within the UI/src directory. UI/src/components directory contains the components that are used in the project.

The String matching module is present in the file Modules/AskUbuntuStringIdfMatch.py file. To view the ML model implementation, navigate to Modules/MLModelInterface and open the file model_interface.py.


