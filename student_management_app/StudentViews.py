import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_management_app.models import Subject, Students, Courses, CustomUser, Attendance, AttendanceReport, \
    LeaveReportStudent, FeedBackStudent


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status = True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status = False).count()
    course = Courses.objects.get(id=student_obj.course_id.id)
    subjects = Subject.objects.filter(course_id=course).count()
    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subject.objects.filter(course_id = student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id = subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance,status = True,student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance,status = False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"student_template/student_home_template.html",{"total_attendance":attendance_total,"attendance_present":attendance_present,"attendance_absent":attendance_absent,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent})

def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    subjects=Subject.objects.filter(course_id = course)
    return render(request,'student_template/student_view_attendance.html',{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_date_parse = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj = Subject.objects.get(id=subject_id)
    user_object = CustomUser.objects.get(id = request.user.id)
    stud_obj = Students.objects.get(admin= user_object)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,end_date_parse),subject_id=subject_id)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,'student_template/student_attendance_data.html',{"attendance_reports":attendance_reports})
    # for attendance_report in attendance_reports:
    #     print("Date : "+str(attendance_report.attendance_id.attendance_date)," Status : "+str(attendance_report.status))


    # return HttpResponse("OK")

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request,'student_template/student_apply_leave.html',{'leave_data':leave_data})

def student_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('student_apply_leave'))
    else:
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date = leave_date, leave_message=leave_message,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied For Leave")
            return HttpResponseRedirect(reverse('student_apply_leave'))
        except:
            messages.error(request, "Failed To Apply For Leave")
            return HttpResponseRedirect(reverse('student_apply_leave'))


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    return render(request,'student_template/student_feedback.html',{'feedback_data':feedback_data})

def student_feedback_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('student_feedback'))
    else:
        feedback_message = request.POST.get("feedback_message")

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStudent(student_id=student_obj, feedback=feedback_message,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse('student_feedback'))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse('student_feedback'))

def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    return render(request,'student_template/student_profile.html',{'user':user,'student':student})

@csrf_exempt
def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse('student_profile'))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get('address')
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            student = Students.objects.get(admin=customuser)
            student.address = address
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse('student_profile'))
        except:
            messages.error(request, "Failed To Update Profile")
            return HttpResponseRedirect(reverse('student_profile'))
