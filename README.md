# TODO_list-app

On the terminal execute the below command to create the projects' working directory and move into that directory.

 
```python
$ mkdir flasktodo
cd flasktodo
```

In the projects' working directory execute the below command to create a virtual environment for our project. Virtual environments make it easier to manage packages for various projects separately.

 
```python
$ virtualenv venv
```

To activate the virtual environment, execute the below command.

```python
$ source venv/Script/activate
```
Clone this repository in the projects' working directory by executing the command below.

```python
$ git clone https://github.com/ajaoooluseyi/todolist.git
$ cd todolist
```

To install all the required dependencies execute the below command.

```python
$ pip install -r requirements.txt
```
This api uses Python version 3.10.6

To run the app, navigate to the app folder in your virtual environment and execute the below command
```python
$ FLASK_APP = app

$ FLASK_ENV = development

$ flask run 
```
