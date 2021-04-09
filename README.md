Task Management  WebApp
=============

>  Helps to organize Tasks and Manage them in one place.

> Better Managing tasks as Private Notes

### Description


- It is a Task Management web app where user can create an account
and make note of tasks that can be done.
- After finished that task either user can mark it as Finished
or Delete from Task List.
-  User can manage their own profiles and tasks with their account.
- When an admin login to the webapp, admin can see about the user statistics 
and user profiles on the Webapp.
- But Tasks are private to the user itself.

### Feautures (user)
- User can register an account.
- Login to his account.
- Create, manage tasks and get organized in one place.
- Inorder to use the webapp, users must have an account.

### Feautures (Admin)
- Only an admin can make other users as admin.
- An Admin can view WebApp User Statistics and other super Feautures.
- Admin can view users profiles (such as name email, date of joining, last login, user current status and others.)
- But No one can view others Tasks, All tasks are private to the users itself.

### Feautures (General)
- By default, When an user register for an account, they will be added to user group of app programatically.
- Tasks are Private to the task owners itself.
- The one who has previllages to access data, can access data. No one can get access to view anything that is not associated with them.(Either User Or Admin Or Individuals)
- Every changes  on the user data will be notified either as success message or as error messages with descriptions.
- Users can't interact with each others through application whereas admins can interact among admin groups by passing admin group messages.


### Run Command (Python)
	`$ pip install -r requirements.txt`

	`$ python manage.py runserver`

### Run Command (Docker Container)
	`$ docker-compose build`

	`$ docker-compose up`