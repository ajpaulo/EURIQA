from cmath import nan
from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from enrollee.models import *
from administrator.models import *
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage

import os
from azure.storage.blob import BlobServiceClient, ContentSettings
# Create your views here.

class EnrolleeHomeView(View):
    def get(self, request):
        return render(request, 'enrollee/enrolleeHome.html')

class EnrolleeLoginView(View):
    def get(self, request):
        return render(request, 'enrollee/enrolleeLogin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            is_enrollee = Enrollee.objects.filter(user_id=request.user.id)

            if is_enrollee:
                return redirect('enrollee:enrollee_details')

            else:
                messages.error(request,"Your account is unauthorized to log in.")
                return redirect("enrollee:enrollee_login")   

        else:
            messages.error(request, 'Invalid username or password.')
            return redirect("enrollee:enrollee_login")

class EnrolleeLogoutView(View):
    def get(self,request):
        logout(request)
        return  redirect("enrollee:enrollee_login")

    def post(self,request):
        logout(request)
        return  redirect("enrollee:enrollee_login")

class EnrolleeDetailsCheckView(View):
    def get(self, request):
        is_enrollee = Enrollee.objects.filter(user_id=request.user.id)

        if request.user.is_authenticated:
            if is_enrollee:
                qs_enrollee = Enrollee.objects.filter(user_id=request.user.id)

                context = {
                    'enrollees' : qs_enrollee,
                }
            else:
                messages.error(request, "You are unauthorized to access this link.")
                return redirect("enrollee:enrollee_login")
        else:
            messages.error(request, "You are not logged in.")
            return redirect("enrollee:enrollee_login")
        return render(request, 'enrollee/enrolleeDetails.html', context)

class EnrolleeTermsView(View):
    def get(self, request):
        is_enrollee = Enrollee.objects.filter(user_id=request.user.id)

        if request.user.is_authenticated:
            if is_enrollee:
                return render(request, 'enrollee/enrolleeTerms.html')
        
            else:
                messages.error(request, "You are unauthorized to access this link.")
                return redirect("enrollee:enrollee_login")
        else:
            messages.error(request, "You are not logged in.")
            return redirect("enrollee:enrollee_login")

class EnrolleeDataPolicyView(View):
    def get(self, request):
        is_enrollee = Enrollee.objects.filter(user_id=request.user.id)
        if request.user.is_authenticated:
            if is_enrollee:
                return render(request, 'enrollee/enrolleeDataPolicy.html')

            else:
                messages.error(request, "You are unauthorized to access this link.")
                return redirect("enrollee:enrollee_login")
        else:
            messages.error(request, "You are not logged in.")
            return redirect("enrollee:enrollee_login")

class EnrolleeCaptureImageView(View):
    def get(self, request):
        is_enrollee = Enrollee.objects.filter(user_id=request.user.id)
        if request.user.is_authenticated:
            if is_enrollee:
                return render(request, 'enrollee/enrolleeCaptureImage.html')

            else:
                messages.error(request, "You are unauthorized to access this link.")
                return redirect("enrollee:enrollee_login")
        else:
            messages.error(request, "You are not logged in.")
            return redirect("enrollee:enrollee_login")
    
    def post(self, request):
        if request.method == 'POST':
            if 'btnNext' in request.POST:
                # picture = request.FILES['picture']
                # fileSystemStorage = FileSystemStorage()
                # filename = fileSystemStorage.save(picture.name, picture)
                # picture = fileSystemStorage.url(filename)
                # update_picture = Enrollee.objects.filter(user_id = request.user.id).update(pictures = picture)
                 # Define connection string from azure
                connect_str = "DefaultEndpointsProtocol=https;AccountName=euriqastorage;AccountKey=DDCCJ4FeaoYFzBDnrtKtf3dY8UFyvBURIT0hUatK6RKwyiRCIC7Q0erwh1llTz/fhWUHHcIISa8dpfIfWW9tbw==;EndpointSuffix=core.windows.net"

                # container name in which images will be store in the storage account
                container_name = "referencephotos" 

                blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
                try:
                    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
                    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
                except Exception as e:
                    print(e)
                    print("Creating container...")
                    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
                
                picture = request.FILES["picture"]
                
                try:
                    set_content_type = ContentSettings(content_type='image/jpeg') # set content type to image
                    container_client.upload_blob(picture.name, picture, content_settings = set_content_type) # upload the photo to the container using the filename as the blob name                    
                    blob_items = container_client.list_blobs()
                    for blob in blob_items:
                        get_blob=container_client.get_blob_client(blob=picture.name)
                        # update_prof_pic = Administrator.objects.filter(user_id = request.user.id).update(picture = get_blob.url)
                
                except Exception as e:
                    print(e)
                    print("Ignoring duplicate filenames") # ignore duplicate filenames
            return redirect("enrollee:enrollee_frtest")

class EnrolleeFaceRecTest(View):
    def get(self, request):
        is_enrollee = Enrollee.objects.filter(user_id=request.user.id)
        if request.user.is_authenticated:
            if is_enrollee:
                return render(request, 'enrollee/enrolleFaceRecTest.html')
                
            else:
                messages.error(request, "You are unauthorized to access this link.")
                return redirect("enrollee:enrollee_login")
        else:
            messages.error(request, "You are not logged in.")
            return redirect("enrollee:enrollee_login")
       
class EnrolleeInstructionsView(View):
    def get(self, request):
        is_enrollee = Enrollee.objects.filter(user_id=request.user.id)
        if request.user.is_authenticated:
            if is_enrollee:
                qs_enrollee = Enrollee.objects.filter(user = request.user.id)
                
                get_level = Enrollee.objects.filter(user = request.user.id).values_list('level', flat=True)
                check_level = Enrollee.objects.filter(user = request.user.id).get(level__in = get_level)
                
                if check_level.level == "college":
                    qs_exam = Exam.objects.filter(takers="College")

                elif check_level.level == "shs":
                    qs_exam = Exam.objects.filter(takers="Senior High School")
                
                elif check_level.level == "jhs":
                    qs_exam = Exam.objects.filter(takers="Junior High School")
                
                elif check_level.level == "elem":
                    qs_exam = Exam.objects.filter(takers="Elementary")
                
                else:
                    print("level does not exist")

                get_exam_id = qs_exam.values_list('exam_id', flat=True)

                qs_part = Part.objects.filter(exam__in = get_exam_id)

                context = {
                    'exams': qs_exam,
                    'enrollee': qs_enrollee,
                    'parts': qs_part,
                }
                return render(request, 'enrollee/enrolleeInstructions.html', context)

            else:
                messages.error(request, "You are unauthorized to access this link.")
                return redirect("enrollee:enrollee_login")
        else:
            messages.error(request, "You are not logged in.")
            return redirect("enrollee:enrollee_login")

def exam_page(request, exam_id=None, part_id=None):
    # Make sure the users are logged in properly
        if request.method != 'POST':
            is_enrollee = Enrollee.objects.filter(user_id=request.user.id)
            if request.user.is_authenticated:
                if is_enrollee:
                
                    # Make sure the examinee is not done taking the exam before redirecting to exam page
                    get_exam_status = Enrollee.objects.filter(user = request.user.id).values_list('exam_status', flat=True)
                    exam_is_done = Enrollee.objects.filter(user = request.user.id).get(exam_status__in = get_exam_status)

                    if exam_is_done.exam_status == 'not done':
                        # Check level of enrollee
                        get_level = Enrollee.objects.filter(user = request.user.id).values_list('level', flat=True)
                        check_level = Enrollee.objects.filter(user = request.user.id).get(level__in = get_level)
                        
                        if check_level.level == "college":
                            qs_exam = Exam.objects.filter(takers="College")

                        elif check_level.level == "shs":
                            qs_exam = Exam.objects.filter(takers="Senior High School")
                        
                        elif check_level.level == "jhs":
                            qs_exam = Exam.objects.filter(takers="Junior High School")
                        
                        elif check_level.level == "elem":
                            qs_exam = Exam.objects.filter(takers="Elementary")
                        
                        else:
                            print("level does not exist")

                        qs_all_parts = Part.objects.filter(exam = exam_id)
                        qs_part = Part.objects.filter(part_id = part_id)
                        qs_question = Question.objects.filter(exam_id = exam_id).filter(part = part_id)
                        qs_question_no = qs_question.values_list('question_no', flat=True)
                        
                        get_last_part = Part.objects.last()

                        context = {
                            'exams': qs_exam,
                            'parts': qs_part,
                            'all_parts': qs_all_parts,
                            'questions': qs_question,
                            'question_no': qs_question_no,
                            'last_part': get_last_part,
                        }

                        return render(request, 'enrollee/enrolleeExam.html', context)
                    
                    else:
                        messages.error(request,"You are already done taking the exam. If you think this is a mistake, contact your enrollment officer.")
                        return redirect("enrollee:enrollee_instructions")
                    
                else:
                    messages.error(request, "You are unauthorized to access this link.")
                    return redirect("enrollee:enrollee_login")
            else:
                messages.error(request, "You are not logged in.")
                return redirect("enrollee:enrollee_login")
                

        else:
            if 'btnSubmitExam' in request.POST:
                # Get question number to append to the answer variable to get all their data from the template
                qs_question_no = Question.objects.filter(exam_id = exam_id).filter(part = part_id).values_list('question_no', flat=True)      
                
                qs_question_id = Question.objects.filter(exam_id = exam_id).filter(part = part_id).values_list('question_id')
                qs_answers = Question.objects.filter(question_id__in = qs_question_id).values_list('answer')
                
                # Get question ids of the exam. This will be used to get the Question instances of each questions from the exam.
                # We need the Question instances for ExamResults has a foreign key field from the Question. 
                get_ques = Question.objects.filter(exam = exam_id).filter(part = part_id).values_list('question_id', flat=True)
                
                # Declare two lists that will receive the answers and the question ids.
                list_answers = []
                list_ques_id = []
                list_correct_ans = []
                # Gets the id of the currently logged in enrollee
                enrollee = request.user.id

                # Get enrollee instance based from the enrollee id
                get_enrollee = Enrollee.objects.get(user_id = enrollee)
                
                # Get exam instance based from the exam id
                get_exam = Exam.objects.get(exam_id = exam_id)

                # Get part instance based from the part id
                get_part = Part.objects.get(part_id = part_id)
                
                # Loop over all the question numbers of their respective parts in the exam
                for idx, num in enumerate(qs_question_no):
                    # The name of the template field for all the answers of the enrollee is "[answer]+[question number]"
                    ques_num="answer"+str(num)

                    # Retrieves all the answers inputted by the enrollee
                    answer = request.POST.get(ques_num)

                    # Stores the retrieved answer from the exam in a list.
                    list_answers.append(answer)
                
                # Loop over all the question records to get their respective instances.
                for ques in Question.objects.filter(question_id__in=get_ques):
                    ques_id = Question.objects.get(question_id = ques.pk)

                    # Store the question instances in the list_ques_id.
                    list_ques_id.append(ques_id)
                    # Store the correct answers in the list_correct_ans.
                    list_correct_ans.append(ques.answer)

                    # try: 
                    # Loop over the list of ques_id to save each inputs from the enrollee to the database.
                    # Since both lists of question id and answer will always have the same number of itemss,
                    # we get the index from one of them to allow easy record saving.
                    # new_results, save_results = ExamResults.objects.update_or_create(enrollee = get_enrollee, exam = get_exam, defaults = {'total_score': total_score})
                    for i in range(len(list_ques_id)):
                        save_items = ExamAnswers(enrollee = get_enrollee, exam = get_exam, part = get_part, is_correct=None, question = list_ques_id[i], answer = list_answers[i])
                    save_items.save()

                    if(list_correct_ans[i] == list_answers[i]):
                        save_items = ExamAnswers.objects.filter(enrollee_id = get_enrollee).filter(question_id = list_ques_id[i]).update(is_correct=True)
                    else:
                        save_items = ExamAnswers.objects.filter(enrollee_id = get_enrollee).filter(question_id = list_ques_id[i]).update(is_correct=False)

                    # # When IntegrityError occurs, just update the database with the same values.
                    # except:
                    #     for i in range(len(list_ques_id)):
                    #         if(list_correct_ans[i] == list_answers[i]):
                    #             save_items = ExamAnswers.objects.filter(question_id = list_ques_id[i]).update(is_correct=True)
                    #         else:
                    #             save_items = ExamAnswers.objects.filter(question_id = list_ques_id[i]).update(is_correct=False)

                # Get the ques ids of correct answers
                get_ques_id = ExamAnswers.objects.filter(enrollee_id = get_enrollee).filter(exam_id = exam_id).filter(is_correct = True).values_list('question_id', flat=True)
                
                # Create a list where we can store all the points of the correct answers
                points_list = []

                # Loop through the question ids of all the correct answer 
                for i in range(len(get_ques_id)):
                    get_points = Question.objects.filter(question_id = get_ques_id[i]).aggregate(Sum('points')).get('points__sum')
                    # Append all points of the correct answer into the list
                    points_list.append(get_points)

                # Get the sum of scores from the list
                total_score = sum(points_list)
                
                # Save/Update Results of Exam for each Part
                new_results, save_results = ExamResults.objects.update_or_create(enrollee = get_enrollee, exam = get_exam, defaults = {'total_score': total_score})

                # Get all part IDs and save it in a list
                get_all = Part.objects.filter(exam_id = exam_id).values_list('part_id', flat=True)
                part_list=list(get_all)
                
                # Append Nonetype at list to serve as stopper when looping through the part ids
                part_list.append(None)

                # Get the ID of the last Part
                last_part = Part.objects.filter(exam_id = exam_id).last()
                
                # Loop over the part ids to properly configure the URLs
                for i in range(len(part_list)):
                    if part_list[i] == part_id or part_list[i-1] != part_id:
                        pass
                        
                    elif (part_list[i] is not None) and (part_list[i] <= last_part.pk or part_list[i] >= last_part.pk):
                        return redirect("enrollee:enrollee_exam", exam_id = exam_id, part_id = part_list[i])
                    else:
                        # Update exam status of enrollee if final part is already answered
                        update_status = Enrollee.objects.filter(user = request.user.id).update(exam_status = "done")
                        return redirect("enrollee:enrollee_examcompletion", enrollee_id=get_enrollee.pk, exam_id = exam_id)

def exam_results(request, enrollee_id=None, exam_id=None):
    if request.method != 'POST':
        is_enrollee = Enrollee.objects.filter(user_id=request.user.id)
        if request.user.is_authenticated:
            if is_enrollee:
            
                get_results = ExamResults.objects.filter(enrollee_id = enrollee_id)
                qs_exams = Exam.objects.filter(exam_id= exam_id)
                qs_parts = Part.objects.filter(exam = exam_id)
                
                # Get the overall_points value from Exam
                get_exam = Exam.objects.get(exam_id = exam_id)
                total_points = get_exam.overall_points

                # Get the total_score value from ExamResults
                get_results = ExamResults.objects.get(enrollee_id = enrollee_id)
                score = get_results.total_score
                
                # Get the passing score (60% passing rate)
                passing_score = total_points*0.60

                # Check if student passed 
                if score >= passing_score:
                    status = "passed"
                
                else:
                    status = "failed"

                score_list = []


                # loop through all question parts
                for qs in qs_parts:
                    # Get question ids of all correct answers
                    correct_ans_id = ExamAnswers.objects.filter(enrollee_id = enrollee_id).filter(exam_id = exam_id).filter(part_id=qs.pk).filter(is_correct=True).values_list('question_id', flat=True)
                    print(correct_ans_id)
        
                    # Get the total points per part
                    total_points_per_part = Question.objects.filter(question_id__in = correct_ans_id).aggregate(Sum('points')).get('points__sum')
                    
                    if total_points_per_part is not None:
                        score_list.append(total_points_per_part)

                    else:
                        total_points_per_part = 0
                        score_list.append(total_points_per_part)

                # Zip the Part objects and the scores for easy displaying in templates
                parts_and_score = zip(qs_parts, score_list)
                
                context={
                    'result' : get_results,
                    'exams': qs_exams,
                    'status': status,
                    'score_list': score_list,
                    'parts_and_score': parts_and_score,
                }
                return render(request, 'enrollee/enrolleeExamCompletion.html', context)

            else:
                messages.error(request, "You are unauthorized to access this link.")
                return redirect("enrollee:enrollee_login")
        else:
            messages.error(request, "You are not logged in.")
            return redirect("enrollee:enrollee_login")