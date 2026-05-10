from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from web.models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Count, Value, CharField
from django.db.models.functions import Lower
from .forms import *   # vào parent folder --> đến forms  from ..
from django.contrib.auth.hashers import make_password
from django.views import View
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# def courses(request):
#     return render(request, 'courses.html')

def team(request):
    return render(request, 'team.html')

def testimonial(request):
    total_students = Student.objects.count()
    context = {'total_students': total_students}
    return render(request, 'testimonial.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('afterlogin')
        else:
            data = {'error': 'Invalid username or password',
            'success': 'success'}
            return render(request, 'login.html', data )

    return render(request, 'login.html')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']
#
#         user = User.objects.create_user(username=username, password=password, email=email)
#         user.save()
#
#         login(request, user)
#
#         group = Group.objects.get_or_create(name='STUDENT')
#         group[0].user_set.add(user)
#
#         return redirect('index')
#
#     return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # Student-specific fields:
        address = request.POST['address']
        mobile = request.POST['mobile']
        enrollment_number = request.POST['enrollment_number']
        #date_of_birth = request.POST['date_of_birth']
        date_of_birth_str = request.POST.get('date_of_birth')
        gender = request.POST['gender']
        profile_pic = request.FILES.get('profile_pic')  # Get uploaded image

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = request.POST.get('first_name', '') # Get first name
            user.last_name = request.POST.get('last_name', '') # Get last name
            user.save()

            login(request, user)  # Log the user in immediately after registration

            group = Group.objects.get_or_create(name='STUDENT')
            group[0].user_set.add(user)

            date_of_birth = date.fromisoformat(date_of_birth_str)

            student = Student.objects.create(
                user=user,
                address=address,
                mobile=mobile,
                enrollment_number=enrollment_number,
                date_of_birth=date_of_birth,
                gender=gender,
                profile_pic=profile_pic, # Save profile pic
            )
            student.save() # This line is necessary for age calculation

            return redirect('index')  # Redirect to the desired page after successful registration

        # except Exception as e:  # Catch potential errors (e.g., duplicate enrollment number)
        #     error_message = str(e)  # Get the error message
        #     # Re-render the form with the error message
        #     return render(request, 'register.html', {'error_message': error_message, 'form_data': request.POST}) # Pass back form data
        except (ValueError, TypeError) as e:  # Handle invalid date format
            error_message = "Invalid date of birth format. Please use YYYY-MM-DD."  # More specific message
            return render(request, 'register.html', {'error_message': error_message, 'form_data': request.POST})
        except ValidationError as e:  # Handle other validation errors
            error_message = str(e)
            return render(request, 'register.html', {'error_message': error_message, 'form_data': request.POST})
        except Exception as e:  # Handle other errors
            error_message = str(e)
            return render(request, 'register.html', {'error_message': error_message, 'form_data': request.POST})

    return render(request, 'register.html') # Handles GET requests and initial form display

def user_logout(request):
    logout(request)
    return redirect('/')

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin(request):
    if is_student(request.user):
        return redirect('index')
    else:
        return redirect('dashboard')

def test(request):
    return render(request, 'test.html')
@login_required(login_url="/login/")
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required(login_url="/login/")
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.POST.get(f'answer_{question.id}')
            print('answer = ', answer)
            print('question.correct_answer = ', question.correct_answer)
            correct =  answer and answer.upper() == question.correct_answer.upper()
            if correct:
                score += 1

        Result.objects.create(
            student=request.user.student,
            quiz=quiz,
            score=score if score else 0
        ) # Assuming 1 point per question
        return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score, 'total': len(questions)})

    return render(request, 'start_quiz.html', {'quiz': quiz, 'questions': questions})

class SubjectListView(LoginRequiredMixin, ListView):  # Inherit from the mixin
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'
    login_url = "/login/" # Or use settings.py LOGIN_URL

class courses(ListView):
    model = Subject
    template_name = 'courses.html'
    context_object_name = 'subjects'

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materials'] = self.object.materials.all()  # Lấy tất cả tài liệu liên quan
        # Lấy tất cả các bài học của môn học này
        context['lessons_in_subject'] = Lesson.objects.filter(subject=self.object.subject)
        return context


##############################            For admin            ##############################
def dashboard(request):
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_lessons = Lesson.objects.count()
    total_documentation = Material.objects.count()
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    students = Student.objects.all()
    
    gender_counts = Student.objects.values('gender').annotate(count=Count('gender'))
    
    gender_data = {
        'Male': 0,
        'Female': 0,
        'Other': 0
    }

    for entry in gender_counts:
        if entry['gender'] == 'M':
            gender_data['Male'] = entry['count']
        elif entry['gender'] == 'F':
            gender_data['Female'] = entry['count']
        elif entry['gender'] == 'O':
            gender_data['Other'] = entry['count']

    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_lessons': total_lessons,
        'total_documentation': total_documentation,
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'students': students,
        'gender_data': gender_data
    }
    return render(request, 'admin_index.html', context)

def admin_blank(request):
    return render(request, 'admin_blank.html')

def summary_report(request):
    results = Result.objects.select_related('student', 'quiz').all()
    students = Student.objects.all()
    quizzes = Quiz.objects.all()

    scores = list(range(11))
    
    # Lọc theo tiêu chí nếu có
    if request.method == 'POST':
        student_id = request.POST.get('student')
        quiz_id = request.POST.get('quiz')
        score = request.POST.get('score')

        if student_id:
            results = results.filter(student_id=student_id)
        if quiz_id:
            results = results.filter(quiz_id=quiz_id)
        if score:
            results = results.filter(score=score)

    context = {
        'results': results,
        'students': students,
        'quizzes': quizzes,
    }
    
    return render(request, 'summary_report.html', context)

def admin_blank(request):
    return render(request, 'admin_blank.html')

def buttons(request):
    return render(request, 'admin_button.html')

def typography(request):
    return render(request, 'admin_typography.html')

def other_element(request):
    return render(request, 'admin_element.html')

def widgets(request):
    return render(request, 'admin_widget.html')

def forms(request):
    return render(request, 'admin_form.html')

def tables(request):
    return render(request, 'admin_table.html')

def charts(request):
    return render(request, 'admin_chart.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.password = make_password(user_form.cleaned_data['password'])  # Hash the password
            user.save()  # Save User first

            # Create or get the STUDENT group
            student_group, created = Group.objects.get_or_create(name='STUDENT')

            # Add user to the STUDENT group
            user.groups.add(student_group)

            student = student_form.save(commit=False)
            student.user = user  # Assign user to student
            student.save()  # Save Student

            return redirect('student_list')

    else:
        user_form = UserForm()
        student_form = StudentForm()

    return render(request, 'student_form.html', {
        'user_form': user_form,
        'student_form': student_form,
    })

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    user = student.user  # Lấy đối tượng User liên kết với Student

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()  # Lưu thông tin User
            student_form.save()  # Lưu thông tin Student
            return redirect('student_list')
    else:
        user_form = UserForm(instance=user)
        student_form = StudentForm(instance=student)

    return render(request, 'student_form.html', {
        'user_form': user_form,
        'student_form': student_form,
        'is_edit': True  # Biến để xác định đây là trang chỉnh sửa
    })


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

def subjects_list(request):
    # Lấy tất cả các môn học
    subjects = Subject.objects.all()

    # Lấy các tham số từ request
    name_filter = request.GET.get('name', '')
    grade_filter = request.GET.get('grade', '')

    # Lọc theo tên môn học nếu có
    if name_filter:
        subjects = subjects.filter(name=name_filter)

    # Lọc theo khối lớp nếu có
    if grade_filter:
        subjects = subjects.filter(grade_level=grade_filter)

    # Lấy danh sách các khối lớp duy nhất từ cơ sở dữ liệu
    grade_levels = Subject.objects.values_list('grade_level', flat=True).distinct()

    return render(request, 'subjects_list.html', {
        'subjects': subjects,
        'name_filter': name_filter,
        'grade_filter': grade_filter,
        'grade_levels': grade_levels,
    })

def subject_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        grade_level = request.POST['grade_level']
        description = request.POST['description']
        image = request.FILES.get('image')
        Subject.objects.create(name=name, grade_level=grade_level, description=description, image=image)
        return redirect('subjects_list')
    return render(request, 'subject_add.html')

def subject_edit(request, id):
    subject = get_object_or_404(Subject, id=id)
    if request.method == 'POST':
        subject.name = request.POST['name']
        subject.grade_level = request.POST['grade_level']
        subject.description = request.POST['description']
        subject.image = request.FILES.get('image', subject.image)  # Nếu không có ảnh mới, giữ nguyên ảnh cũ
        subject.save()
        return redirect('subjects_list')
    return render(request, 'subject_edit.html', {'subject': subject})

def subject_delete(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()
    return redirect('subjects_list')
    
from django.shortcuts import render
from django.views import View
from .models import Lesson, Subject

class LessonListView(View):
    def get(self, request):
        subject_id = request.GET.get('subject', '')
        
        # Lấy danh sách các môn học để hiển thị trong dropdown
        subjects = Subject.objects.all()  
        
        # Lọc các bài học theo môn học nếu có subject_id
        if subject_id:
            lessons = Lesson.objects.filter(subject_id=subject_id)  # Lọc theo môn học
        else:
            lessons = Lesson.objects.all()  # Lấy tất cả các bài học nếu không có bộ lọc
        
        return render(request, 'lesson_list.html', {
            'lessons': lessons,
            'subjects': subjects,
            'subject_id': subject_id
        })

class LessonAddView(View):
    def get(self, request):
        subjects = Subject.objects.all()  # Lấy tất cả các môn học
        return render(request, 'lesson_add.html', {'subjects': subjects})

    def post(self, request):
        subject_id = request.POST.get('subject')
        lesson_number = request.POST.get('lesson_number')
        description = request.POST.get('description')
        youtube_link = request.POST.get('youtube_link')

        # Tạo và lưu bài học mới
        lesson = Lesson(
            subject_id=subject_id,
            lesson_number=lesson_number,
            description=description,
            youtube_link=youtube_link
        )
        lesson.save()
        messages.success(request, 'Lesson added successfully!')
        return redirect('lesson_list')

class LessonEditView(View):
    def get(self, request, id):
        lesson = get_object_or_404(Lesson, id=id)  # Lấy bài học theo ID
        subjects = Subject.objects.all()  # Lấy tất cả các môn học
        return render(request, 'lesson_edit.html', {'lesson': lesson, 'subjects': subjects})

    def post(self, request, id):
        lesson = get_object_or_404(Lesson, id=id)  # Lấy bài học theo ID
        lesson.subject_id = request.POST.get('subject')
        lesson.lesson_number = request.POST.get('lesson_number')
        lesson.description = request.POST.get('description')
        lesson.youtube_link = request.POST.get('youtube_link')
        lesson.save()
        messages.success(request, 'Lesson updated successfully!')
        return redirect('lesson_list')

class LessonDeleteView(View):
    def post(self, request, id):
        lesson = get_object_or_404(Lesson, id=id)  # Lấy bài học theo ID
        lesson.delete()  # Xóa bài học
        messages.success(request, 'Lesson deleted successfully!')
        return redirect('lesson_list')

def documentation_list(request):
    # Lấy danh sách các môn học để hiển thị trong dropdown
    subjects = Subject.objects.all()
    
    # Lấy ID môn học từ query parameter
    subject_id = request.GET.get('subject', '')

    # Lọc tài liệu theo môn học nếu có
    if subject_id:
        materials = Material.objects.filter(lesson__subject_id=subject_id)
    else:
        materials = Material.objects.all()
        
    return render(request, 'documentation_list.html', {
        'materials': materials,
        'subjects': subjects,  # Truyền danh sách môn học vào template
    })

def documentation_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    lessons = Lesson.objects.all()  # Lấy tất cả các lesson

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('documentation_list')
    else:
        form = MaterialForm(instance=material)
    
    return render(request, 'documentation_form.html', {
        'form': form,
        'title': 'Edit Document',
        'lessons': lessons,
        'selected_lesson': material.lesson  # Giữ lại lesson đã chọn
    })

def documentation_add(request):
    lessons = Lesson.objects.all()  # Lấy tất cả các lesson

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)  # Không lưu ngay
            lesson_id = request.POST.get('lesson')  # Lấy ID của lesson từ form
            material.lesson = Lesson.objects.get(id=lesson_id)  # Gán lesson cho material
            material.save()  # Lưu material
            return redirect('documentation_list')
    else:
        form = MaterialForm()
    
    return render(request, 'documentation_form.html', {
        'form': form,
        'title': 'Add Document',
        'lessons': lessons
    })

def documentation_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == 'POST':
        material.delete()
        return redirect('documentation_list')  # Quay lại danh sách tài liệu

    return render(request, 'documentation_confirm_delete.html', {'material': material})

def quiz_overviews(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_overview.html', {'quizzes': quizzes})  # Cập nhật tên file

def quiz_add(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_overviews')
    else:
        form = QuizForm()
    return render(request, 'quiz_form.html', {'form': form, 'title': 'Add Quiz'})

def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_overviews')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz_form.html', {'form': form, 'title': 'Edit Quiz'})

def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz has been deleted successfully.')
        return redirect('quiz_overviews')  # Đảm bảo tên URL chính xác
    
def question_list(request):
    quiz_filter = request.GET.get('quiz_filter')
    questions = Question.objects.all()  # Start with all questions

    # Check if the filter is set and is not 'all'
    if quiz_filter and quiz_filter != 'all':
        questions = questions.filter(quiz__id=quiz_filter)  # Filter by quiz ID

    quizzes = Quiz.objects.all()  # Get all quizzes

    return render(request, 'question_list.html', {
        'questions': questions,
        'quizzes': quizzes,  # Pass the list of quizzes to the template
        'selected_quiz_id': quiz_filter  # Pass the selected quiz ID to the template
    })

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'add_edit_question.html', {'form': form})

def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)  # Lấy câu hỏi dựa trên ID
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)  # Gán câu hỏi hiện tại vào form
        if form.is_valid():
            form.save()  # Lưu thay đổi
            return redirect('question_list')  # Quay lại danh sách câu hỏi
    else:
        form = QuestionForm(instance=question)  # Tạo form với dữ liệu hiện tại
    return render(request, 'add_edit_question.html', {'form': form})  # Trả về template với form

def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)  # Lấy câu hỏi dựa trên ID
    if request.method == 'POST':
        question.delete()  # Xóa câu hỏi
        return redirect('question_list')  # Quay lại danh sách câu hỏi
    return render(request, 'confirm_delete.html', {'question': question})  # Hiển thị trang xác nhận xóa

def test_student(request):
    students = Student.objects.all()  # Fetch all students
    return render(request, 'test_student.html', {'students': students})

def gender_distribution(request):
    gender_counts = Student.objects.values('gender').annotate(count=Count('gender'))
    
    gender_data = {
        'Male': 0,
        'Female': 0,
        'Other': 0
    }

    for entry in gender_counts:
        if entry['gender'] == 'M':
            gender_data['Male'] = entry['count']
        elif entry['gender'] == 'F':
            gender_data['Female'] = entry['count']
        elif entry['gender'] == 'O':
            gender_data['Other'] = entry['count']
    
    return render(request, 'gender_distribution.html', {'gender_data': gender_data})

def new_dashboard(request):
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_lessons = Lesson.objects.count()
    total_documentation = Material.objects.count()
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    students = Student.objects.all()   # lay het du lieu

    context = {
        'total_students_html': total_students,
        'total_subjects_html': total_subjects,
        'total_lessons_html': total_lessons,
        'total_documentation_html': total_documentation,
        'total_quizzes_html': total_quizzes,
        'total_questions_html': total_questions,
        'students_html': students,
    }
    # context la thanh phan du lieu dong se truyen qua html 

    return render (request, 'new_dashboard.html', context)

def new_add_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        print('---test 1')

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.password = make_password(user_form.cleaned_data['password'])  # Hash the password
            user.save()  # Save User first
            print('---test 2')

            # Create or get the STUDENT group
            student_group, created = Group.objects.get_or_create(name='STUDENT')

            # Add user to the STUDENT group
            user.groups.add(student_group)
            print('---test 3')

            student = student_form.save(commit=False)
            student.user = user  # Assign user to student
            student.save()  # Save Student
            print('---test 4')

            return redirect('student_list')

    else:
        user_form = UserForm()
        student_form = StudentForm()
        print('---test 5')

    return render(request, 'new_add_student.html', {
        'user_form': user_form,
        'student_form': student_form,
    })