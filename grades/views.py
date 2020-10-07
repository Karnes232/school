from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
import xlwt


from .forms import PasswordChangingForm
from .models import User, Teacher, Student, Courses, Grades
from .util import SuperUser, TeacherUser, StudentUser

#Allows users to change password
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    #Checks current user (Prinipal, Teacher, or Student)
    current_user = request.user.get_username()
    is_super = SuperUser(current_user)
    is_teacher = TeacherUser(current_user)
    is_student = StudentUser(current_user)
    return render(request, "grades/password_success.html", {
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student
        })

#Login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "grades/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "grades/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

#Create new student or teacher
@login_required(login_url='login')
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        telephone = request.POST["telephone"]
        position = request.POST["position"]
        email = request.POST["email"]
        print(position)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "grades/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "grades/register.html", {
                "message": "Username already taken."
            })       
        #Puts created user in catagory of teacher or student
        try:
            if position == "Teacher":
                user_id = User.objects.get(username=username)
                teacher = Teacher(user=user_id, last_name=last_name, first_name=first_name, telephone=telephone)
                teacher.save()
                user_id.is_teacher = True
                user_id.save()
            elif position == "Student":
                user_id = User.objects.get(username=username)
                student = Student(user=user_id, last_name=last_name, first_name=first_name, telephone=telephone)
                student.save()
                user_id.is_student = True
                user_id.save()
        except:
            pass
        return HttpResponseRedirect(reverse("index"))
    else:
        #Checks current user (Prinipal, Teacher, or Student)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        return render(request, "grades/register.html", {
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student
        })

@login_required(login_url='login')
def index(request):
    #Checks current user (Prinipal, Teacher, or Student)
    current_user = request.user.get_username()
    is_super = SuperUser(current_user)
    is_teacher = TeacherUser(current_user)
    is_student = StudentUser(current_user)
    return render(request, "grades/index.html", {
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student
        })

@login_required(login_url='login')
def create_course(request):
    if request.method == "POST":
        #Takes input and selected teacher to create a course
        course = request.POST["course"]
        teacher = request.POST["teacher"]
        c = Courses(subject=course, teacher_id=teacher)
        c.save()
        #Checks current user and all listed teachers
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        teachers = Teacher.objects.all()
        return render(request, "grades/create-course.html", {
            "is_super": is_super,
            "teachers": teachers,
            "message": "Course Created"
        })

    else:
        #Checks current user and all listed teachers
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        teachers = Teacher.objects.all()
        return render(request, "grades/create-course.html", {
            "is_super": is_super,
            "teachers": teachers,
        })

@login_required(login_url='login')
def courses(request):
    if request.method == "POST":
        pass

    else:
        #Lists all courses for prinipal
        #If user is teacher lists their courses
        current_user = request.user
        teacher = Teacher.objects.filter(user=current_user.id)
        user_courses = []
        for t in teacher:
            user_courses = Courses.objects.filter(teacher=t.id)
        courses = Courses.objects.all()
        #Checks current user (Prinipal, Teacher, or Student)
        
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        return render(request, "grades/course-list.html", {
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student,
            "courses": courses,
            "user_courses": user_courses
        })

@login_required(login_url='login')
def course(request, course_id):
    if request.method == "POST":
        #Adds Student to Course
        add_student = request.POST["student"]
        student = Student.objects.get(id=add_student)
        student.courses.add(course_id)
        #student.courses.remove(course_id)
        #Adds student and course to grades model
        course = Courses.objects.get(id=course_id)
        grades = Grades(student=student, course=course)
        grades.save()

        #Gets list of students enrolled and not enrolled
        course = Courses.objects.get(id=course_id)
        non_students = Student.objects.exclude(courses=course).all()        
        students = Grades.objects.filter(course=course)
        
        #Checks current user (Prinipal, Teacher, or Student)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        return render(request, "grades/course.html", {
            "course": course,
            "non_students": non_students,
            "students": students,
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student,
        })

    else:
        course = Courses.objects.get(id=course_id)
        non_students = Student.objects.exclude(courses=course).all()
        #students = Student.objects.filter(courses=course)
        students = Grades.objects.filter(course=course)
        #Checks current user (Prinipal, Teacher, or Student)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        return render(request, "grades/course.html", {
            "course": course,
            "non_students": non_students,
            "students": students,
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student,  
                      
        })

@login_required(login_url='login')
def student(request, student_id):
    #Allows teacher to edit grades
    if request.method == "POST":
        course_id = request.POST["id"]
        grades = Grades.objects.filter(id=course_id)
        return render(request, "grades/grading.html", {
            "grades": grades
        })
    else:
        grades = Grades.objects.filter(student=student_id)
        student = Student.objects.get(id=student_id)
        
        #Checks current user (Prinipal, Teacher, or Student)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        return render(request, "grades/student.html", {
            "student": student,
            "grades": grades,
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student,
        })

@login_required(login_url='login')
def grades(request):
    if request.method == "POST":
        #Updates students grades for course
        grade_id = request.POST["grade_id"]
        t1_p1 = request.POST["t1_p1"]
        t1_p2 = request.POST["t1_p2"]
        t1_p3 = request.POST["t1_p3"]
        t2_p1 = request.POST["t2_p1"]
        t2_p2 = request.POST["t2_p2"]
        t2_p3 = request.POST["t2_p3"]
        t3_p1 = request.POST["t3_p1"]
        t3_p2 = request.POST["t3_p2"]
        t3_p3 = request.POST["t3_p3"]
        updating_grades = Grades.objects.get(id=grade_id)
        updating_grades.t1_p1 = t1_p1
        updating_grades.t1_p2 = t1_p2
        updating_grades.t1_p3 = t1_p3
        updating_grades.t2_p1 = t2_p1
        updating_grades.t2_p2 = t2_p2
        updating_grades.t2_p3 = t2_p3
        updating_grades.t3_p1 = t3_p1
        updating_grades.t3_p2 = t3_p2
        updating_grades.t3_p3 = t3_p3
        updating_grades.save()
        student = request.POST["student"]
        grades = Grades.objects.filter(student=student)
        #Checks current user (Prinipal, Teacher, or Student)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        return render(request, "grades/student.html", {
            "grades": grades,
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student,
        })
    else:
        pass

@login_required(login_url='login')
def report(request):
    if request.method == "POST":
        pass
    else:
        #Checks current user (Prinipal, Teacher, or Student)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        user = User.objects.get(username=current_user)
        user = user.id
        student = Student.objects.filter(user=user)
        grades = []
        for s in student:
            grades = Grades.objects.filter(student=s)
        return render(request, "grades/student.html", {
            "student": student,
            "grades": grades,
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student,
        })

@login_required(login_url='login')
def report_all(request):
    if request.method == "POST":
        pass
    else:
        #Checks current user (Prinipal, Teacher, or Student)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_teacher = TeacherUser(current_user)
        is_student = StudentUser(current_user)
        students = Student.objects.all().order_by("last_name")
        return render(request, "grades/student-list.html", {
            "students": students,
            "is_super": is_super,
            "is_teacher": is_teacher,
            "is_student": is_student,
        })

@login_required(login_url='login')
def individual(request, student_id):
    #Checks current user (Prinipal, Teacher, or Student)
    current_user = request.user.get_username()
    is_super = SuperUser(current_user)
    is_teacher = TeacherUser(current_user)
    is_student = StudentUser(current_user)
    #Gets Students info and displays grades
    student = Student.objects.get(id=student_id)
    grades = Grades.objects.filter(student=student_id)
    return render(request, "grades/student.html", {
        "student": student,
        "grades": grades,
        "is_super": is_super,
        "is_teacher": is_teacher,
        "is_student": is_student,
    })

@login_required(login_url='login')
def course_report(request):
    course_id = request.POST["course_id"]
    course = Courses.objects.get(id=course_id)
    grades = Grades.objects.filter(course_id=course_id)
    #Checks current user (Prinipal, Teacher, or Student)
    current_user = request.user.get_username()
    is_super = SuperUser(current_user)
    is_teacher = TeacherUser(current_user)
    is_student = StudentUser(current_user)
    return render(request, "grades/report.html", {
        "course": course,
        "grades": grades,
        "is_super": is_super,
        "is_teacher": is_teacher,
        "is_student": is_student,
    })

def export_users_xls(request):
    course_id = request.POST["course_id"]
    print(course_id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % course_id

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Student', 'T1-P1', 'T1-P2', 'T1-P3', 'T2-P1', 'T2-P2', 'T2-P3', 'T3-P1', 'T3-P2', 'T3-P3', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    grades = Grades.objects.filter(course_id=course_id).values_list('student', 't1_p1', 't1_p2', 't1_p3', 't2_p1', 't2_p2', 't2_p3', 't3_p1', 't3_p2', 't3_p3')
    #rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in grades:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_users_xls2(request):
    student_id = request.POST["student_id"]
    print(student_id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % student_id

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Course', 'T1-P1', 'T1-P2', 'T1-P3', 'T2-P1', 'T2-P2', 'T2-P3', 'T3-P1', 'T3-P2', 'T3-P3', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    grades = Grades.objects.filter(student_id=student_id).values_list('course', 't1_p1', 't1_p2', 't1_p3', 't2_p1', 't2_p2', 't2_p3', 't3_p1', 't3_p2', 't3_p3')
    #rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in grades:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

