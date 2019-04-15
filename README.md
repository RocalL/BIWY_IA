# BIWY_IA
IA part of BIWY project


# Get Started : 
This project is a fork of https://github.com/ageitgey/face_recognition. 
Please look at the requirements there before using BIWY_IA. 

There are two main script : 
* train_script.py 
* launch_script.py

You can also find a database access script : bdd_access.py

# How does it work ? 

The IA part of BIWY is used to train a face recognition model and use it to check people presence. 

If you are using BIWY_IA across the front web interface (https://github.com/MohamedKourouma/BIWY) you can manage people and checkpoints. Nevertheless, you can use BIWY_IA as a standalone app by adding to a "img" directory, pictures of people you want to check presence. 

# Step 
## 1 : train part 
Train the model and associate people with their pictures

`python2 train_script.py`
## 2 : launch part
Launch a video catpure program that recognize known people and save the datetime in database

`python2 launch_script.py`
