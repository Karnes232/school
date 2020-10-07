from .models import User

def SuperUser(current_user):
    superusers = User.objects.filter(is_superuser=True)
    current_id = User.objects.get(username=current_user)
    is_super = False
    for su in superusers:
        if current_id == su:
            is_super = True
    return is_super


def TeacherUser(current_user):
    teacher = User.objects.filter(is_teacher=True)
    current_id = User.objects.get(username=current_user)
    is_teacher = False
    for t in teacher:
        if current_id == t:
            is_teacher = True
    return is_teacher

def StudentUser(current_user):
    student = User.objects.filter(is_student=True)
    current_id = User.objects.get(username=current_user)
    is_student = False
    for s in student:
        if current_id == s:
            is_student = True
    return is_student