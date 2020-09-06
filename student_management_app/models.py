from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Overwriting the Default Django Auth User and Adding One More Field in This Model which is User type
# User Type 1: Admin,
# User Type 2: Staff,
# User Type 3: Student

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"),(2, "Staff"),(3,"Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length = 10)

# Now Normalizing the Student, Staff, HOD Model by Removing Name, Password, Email Because This Information Already Storing into Default Django User Which is CustomUser

# Then delete the database and migration folder

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")
    objects=models.Manager()

class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    #mapping courses to subjects
    objects = models.Manager()

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    # now mapping to courses
    course_id=models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    # now we will map subjects with faculty
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    object = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    address= models.TextField()
    course_id = models.ForeignKey(Courses, on_delete = models.DO_NOTHING)
    # Adding Session Start and End Year for students
    session_year_id = models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")
    # Now I want to create courses
    objects = models.Manager()

class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks=models.FloatField(default=0)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    objects = models.Manager()


# Now creating Attendance model
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete = models.DO_NOTHING)
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    session_year_id = models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

# Now creating attendance report model
class AttendanceReport(models.Model):
    id = models.AutoField(primary_key = True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

# LeaveReport model for students
class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key = True)
    student_id = models.ForeignKey(Students, on_delete = models.CASCADE)
    leave_date = models.CharField(max_length = 255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

# LeaveReport model for staff members
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key = True)
    staff_id = models.ForeignKey(Staff, on_delete = models.CASCADE)
    leave_date = models.CharField(max_length = 255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

# Student Feedback model
class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete = models.CASCADE)
    feedback = models.CharField(max_length = 255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

# staff feedback model
class FeedBackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete = models.CASCADE)
    feedback = models.CharField(max_length = 255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

# creating Student Notification model
class NotificationStudent(models.Model):
    id = models.AutoField(primary_key = True)
    student_id = models.ForeignKey(Students, on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

# Creating Staff Notification model
class NotificationStaff(models.Model):
    id = models.AutoField(primary_key = True)
    staff_id = models.ForeignKey(Staff, on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

# Now Creating Signal in Django So When New User Create I Will add a New Row in HOD, Staff, Student With it's ID in admin_id Column

# Creating @reciever(post_save, sender=CustomUser)
# So this Method will run only when data added in CustomUser

@receiver(post_save, sender=CustomUser)

# Now Creating a Function which add Data into HOD, Staff, Student Table

def create_user_profile(sender, instance, created, **kwargs):

# Taking Parameter sender, instance, created Here Sender is Class Which Call this Method instance is Current Inserted Data Model created is True/False, True when Data Inserted
    if created:
    # if created is True Means Data Inserted
            if instance.user_type == 1:
            # Then I will Insert Data into Other Table
            # if user_type = 1 Then I will add Row in HOD Table with Admin ID
                AdminHOD.objects.create(admin = instance)
            if instance.user_type == 2:
            # Now calling the Staff.objects.create() and passing admin=instance When User Type is 2
                Staff.objects.create(admin=instance, address="")
            if instance.user_type==3:
            # similarly calling the Student.objects.create()) and passing admiin = instance when user Type is 3
                Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1), session_year_id = SessionYearModel.object.get(id=1), address="",profile_pic="",gender="")
# Now we will call after create_user_profile()
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staff.save()
    if instance.user_type==3:
        instance.students.save()
    # So all this reciever work when we add new data in custom user table after inserting data i will insert the current id of customuser into other table such as adminhod, staff, students