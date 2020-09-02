from django.contrib import messages
from django.core import serializers
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Subject, SessionYearModel, Students, Attendance, AttendanceReport, LeaveReportStaff, Staff, \
    FeedBackStaff, CustomUser, Courses


def staff_home(request):
    # For Fetch ALL Student Under Staff
    subjects = Subject.objects.filter(staff_id = request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id = subject.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    # removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(course_id__in=final_course).count()
    #Fetch ALL Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    #Fetch ALL Approve Leave
    staff = Staff.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id = staff.id,leave_status=1).count()
    #Fetching ALL Subjects Count
    subjects_count = subjects.count()
    #Fetch Attendance Data by Subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(status=True,
                                                                   student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False,
                                                                  student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)
    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"subjects_count":subjects_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})

def staff_take_attendance(request):
    subjects = Subject.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject = Subject.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data = []
    for student in students:
        data_small = {"id": student.admin.id, "name": student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")
    subject_model = Subject.objects.get(id = subject_id)
    session_model = SessionYearModel.object.get(id = session_year_id)
    json_sstudent=json.loads(student_ids)
    # print(data[0]['id'])

    try:
        attendance = Attendance(subject_id= subject_model,session_year_id=session_model,attendance_date=attendance_date)
        attendance.save()
        print(student_ids)
        for stud in json_sstudent:
            student=Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")

def staff_update_attendance(request):
    subjects = Subject.objects.filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.object.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subject.objects.get(id = subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id = subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data = {'id':attendance_single.id, "attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []
    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    json_sstudent=json.loads(student_ids)

    try:
        for stud in json_sstudent:
            student=Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
            attendance_report.status= stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")

def staff_apply_leave(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request,'student_template/student_apply_leave.html',{'leave_data':leave_data})

def staff_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('staff_apply_leave'))
    else:
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")

        staff_obj = Staff.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date = leave_date, leave_message=leave_message,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied For Leave")
            return HttpResponseRedirect(reverse('staff_apply_leave'))
        except:
            messages.error(request, "Failed To Apply For Leave")
            return HttpResponseRedirect(reverse('staff_apply_leave'))


def staff_feedback(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    return render(request,'staff_template/student_feedback.html',{'feedback_data':feedback_data})

def staff_feedback_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('staff_feedback'))
    else:
        feedback_message = request.POST.get("feedback_message")

        staff_obj = Staff.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStaff(staff_id=staff_obj, feedback=feedback_message,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse('staff_feedback'))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse('staff_feedback'))

def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staff.objects.get(admin = user)
    return render(request,'staff_template/staff_profile.html',{'user':user,'staff':staff})

@csrf_exempt
def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse('staff_profile'))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            staff = Staff.objects.get(admin=customuser)
            customuser.first_name = first_name
            customuser.last_name = last_name
            staff.address = address

            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Procfile")
            return HttpResponseRedirect(reverse('staff_profile'))
        except:
            messages.error(request, "Failed To Update Procfile")
            return HttpResponseRedirect(reverse('staff_profile'))

