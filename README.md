SMART ATTENDANCE MANAGEMENT SYSTEM USING FACE RECOGNITION

OVERVIEW
The Smart Attendance Management System is a web-based application that automates student attendance using face recognition technology. The system reduces manual effort, avoids proxy attendance, and provides accurate attendance records in real time.
The project is developed using Python and Django, integrated with OpenCV and the face_recognition library for facial recognition, and PostgreSQL for secure data storage.

OBJECTIVES

•	Automate the attendance process

•	Reduce manual errors

•	Prevent proxy attendance

•	Manage attendance course-wise and semester-wise

•	Generate attendance reports efficiently

FEATURES

•	Student registration with face image

•	Real-time face detection using camera

•	Automatic attendance marking

•	Course and semester-based attendance sessions

•	Admin dashboard with reports and analytics

•	Download attendance records

TECHNOLOGIES USED

•	Programming Language: Python

•	Framework: Django

•	Libraries: OpenCV, face_recognition, NumPy, Pillow

•	Frontend: HTML, CSS, JavaScript, Bootstrap

•	Database: PostgreSQL

SYSTEM WORKFLOW

•	Admin starts attendance session by selecting course and semester

•	Camera captures student face

•	Face is detected and recognized

•	Attendance is marked automatically

•	Records are stored in the database

•	Admin views attendance reports

INSTALLATION AND SETUP

•	git clone https://github.com/Anfas007/smart-attendance-management-system.git

•	cd smart-attendance-system

•	python -m venv venv

•	venv\Scripts\activate

•	pip install -r requirements.txt

•	python manage.py makemigrations

•	python manage.py migrate

•	python manage.py runserver

FUTURE ENHANCEMENTS

•	Mobile application support

•	Cloud database integration

•	SMS and email notifications

•	Multi-camera support

•	Improved recognition accuracy

CONCLUSION

The Smart Attendance Management System provides an efficient and secure solution for attendance management using AI-based face recognition. It is suitable for educational institutions seeking automation and accuracy.

