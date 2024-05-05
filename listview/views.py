from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.db.models import Q
from listview.models import Base_Email, Login_Details, Client
from django.views import View
import json
# from linkedin_api import Linkedin, linkedin
from requests.cookies import cookiejar_from_dict
import smtplib
from email.message import EmailMessage
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
# from users_models import CustomUser
import users.models as users_models
# import csv
from .models import MediaStorage
from multiprocessing.pool import ThreadPool
# import os
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib import messages
import boto3
import http.client
import mimetypes
# import mimetypes
# Create your views here.
s3_client = boto3.client("s3",
                         region_name='ap-south-1',
                         aws_access_key_id='',
                         aws_secret_access_key='')


@login_required
def index(request):

    if request.method == "GET":

        droppedid = request.GET.get("droppedid")
        droppedstatus = request.GET.get("droppedstatus")
        if droppedid and droppedstatus:
            status_item = Client.objects.get(id=droppedid)
            status_item.task_status = droppedstatus
            status_item.save()

    if request.method == "POST":

        try:
            username = request.POST['username']
        except:
            username = ""
        try:

            email = request.POST['email']
        except:
            email = ""
        try:

            phone = request.POST['phone']
        except:
            phone = ""
        try:

            company = request.POST['company']
        except:
            company = ""
        try:

            certificate_name = request.POST['certificate_name']
        except:
            certificate_name = ""
        try:

            title = request.POST['title']
        except:
            title = ""
        try:

            certificate_type = request.POST['certificate_type']
        except:
            certificatae_type = ""
        try:

            description = request.POST['description']
        except:
            description = ""

        ins = Client(certificate_name=certificate_name, title=title, company=company, certificate_type=certificate_type, name=username, user_mail=email, description=description,
                     phone=phone)
        try:

            uploads = request.POST["new_show_uploads"]
            if uploads:
                ins.upload = uploads
        except:
            pass

        ins.save()

        return redirect('/')
    if request.user.is_superuser:
        todos = Client.objects.filter(task_status="Hold")
        progress = Client.objects.filter(task_status="Progress")
        review = Client.objects.filter(task_status="Review")
        approved = Client.objects.filter(task_status="Approved")
    else:
        todos = Client.objects.filter(
            task_status="Hold", user_mail=request.user.email)
        progress = Client.objects.filter(
            task_status="Progress", user_mail=request.user.email)
        review = Client.objects.filter(
            task_status="Review", user_mail=request.user.email)
        approved = Client.objects.filter(
            task_status="Approved", user_mail=request.user.email)
    # allData = Client.objects.all()
    b_mails = Base_Email.objects.all()
    if request.method == "GET":
        st = request.GET.get("search-name")
        if st != None:
            if request.user.is_superuser:
                todos = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Hold")
                progress = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Progress")
                review = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Review")
                approved = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Approved")
            else:
                todos = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Hold", user_mail=request.user.email)
                progress = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Progress", user_mail=request.user.email)
                review = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Review", user_mail=request.user.email)
                approved = Client.objects.filter((Q(name__icontains=st) | Q(title__icontains=st) | Q(
                    certificate_type__icontains=st) | Q(company__icontains=st) | Q(
                    certificate_name__icontains=st)), task_status="Approved", user_mail=request.user.email)

    context = {
        'emails': b_mails,
        "todos": todos,
        "progress": progress,
        "review": review,
        "approved": approved}
    return render(request, 'listview/base.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
@login_required
def example(request):
    return HttpResponse('Welcome to Example.')


@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
@login_required
def createUser(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        access_level = request.POST["access-level"]
        new_user = users_models.CustomUser.objects.create_user(
            email=email, username=name, password=password)
        new_user.approvals = 1
        if access_level == 'Admin':
            new_user.is_superuser = 1
            new_user.is_staff = 1

        else:
            new_user.is_superuser = 0
            new_user.is_staff = 0

        new_user.save()
        print('new user created')
    return redirect('/')


def approveUser(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        phone = request.POST["phone"]
        company = request.POST["company"]
        already_there = users_models.CustomUser.objects.filter(
            email=email).exists()
        if name == '' or email == '' or password1 == '' or phone == '' or company == '':
            messages.error(request, "Fields should not be empty")
            return redirect('/signup')
        elif already_there:
            messages.error(request, "Email already exists")
            return redirect('/signup')
        else:
            # access_level = request.POST["access-level"]
            new_user = users_models.CustomUser.objects.create_user(
                email=email, username=name, password=password1, phone=phone, company=company)
            new_user.is_superuser = 0
            new_user.is_staff = 0
            # new_user.approval = 0
            new_user.save()
            print('new user created')
            messages.warning(
                request, "Your account is sent for approval. Please Login after some time.")
            return redirect('/user/login')


def signup(request):
    return render(request, 'listview/register.html')


@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
@login_required
def approvals(request):
    allUsers = users_models.CustomUser.objects.filter(approvals=0)
    context = {'users': allUsers}
    return render(request, 'listview/approvals.html', context)


def approve_new_user(request):
    if request.method == "POST":

        email = request.POST["email"]
        user = users_models.CustomUser.objects.get(email=email)
        user.approvals = 1
        user.save()
    return HttpResponse("Done")


def delete_new_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = users_models.CustomUser.objects.get(email=email)
        user.delete()
    return HttpResponse("Done")


class Delete(View):
    @method_decorator(login_required)
    # @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None))
    def post(self, request):
        if request.method == "POST":
            data = request.POST["name"]
            record = Client.objects.get(id=data)
            record.delete()
        return redirect('/')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def delete_user(request):
    if request.method == "POST":
        data = request.POST
        user = users_models.CustomUser.objects.get(email=data["name"])

        records = Client.objects.filter(user_mail=data["name"])
        try:
            for i in records:
                i.delete()
        except:
            pass
        user.delete()
    return HttpResponse("done")


@login_required
def massmail(request):
    if request.method == 'POST':

        # sender = request.POST["sender"]
        # # sender = 'frazorf302@gmail.com'
        # recipients = request.POST["recipient"]
        # sender_details = Base_Email.objects.get(b_email=sender)

        # msg = EmailMessage()
        # msg['Subject'] = request.POST["subject"]
        # msg['From'] = sender_details.b_email
        # # msg['Bcc'] = ', '.join(recipients) # all the contacts separated by a comma
        # msg['Bcc'] = recipients
        # msg.set_content(request.POST["body"])

        # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        #     smtp.login(sender_details.b_email, sender_details.b_pass)
        #     smtp.send_message(msg)

        recipients = request.POST["recipient"]
        recipients = recipients.replace(",", "")
        print("recipient: ", recipients)
        recipients_list = recipients.split()
        print("recipients_list: ", recipients_list)
        recipients_list = json.dumps(recipients_list)
        subject = request.POST["subject"]
        body = request.POST["body"]
        conn = http.client.HTTPSConnection("api.mailazy.com")
        payload = (f"""{{"to": {recipients_list}, "from": "Sender@flookup.co.in", "subject": "{subject}", "content": [{{"type": "text/plain","value": "{body}"}}]}}""")
        print(payload)
        headers = {
            'X-Api-Key': 'c7hf4l2dc007534ff8qgEHjqQUiSsj',
            'X-Api-Secret': ' FSjYwMfBDJlUXBUAttOtGBmfjvUOuBrwMEiuhYNd.WDWYxiTw2Zj6dh42TxSfPD',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/mail/send", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    return redirect('/')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def users(request):
    param = request.GET.get('search-user')
    if param is not None:
        allUsers = users_models.CustomUser.objects.filter(
            username__icontains=param)
    else:
        allUsers = users_models.CustomUser.objects.all()
    context = {'users': allUsers}
    return render(request, 'listview/users.html', context)


# @login_required
# def autofill(request):
#     if request.method == 'GET':
#         print('received data')
#         print(request.GET['input_value'])
#         post_data = request.GET['input_value']
#         user_id = post_data.split('/')[4]
#         scraped_details = get_linkedin_data(user_id)
#         jsonified_details = json.dumps(scraped_details)
#         print(jsonified_details)
#         return HttpResponse(jsonified_details, content_type="text/json")
#         # return redirect('/')
#     return HttpResponse('Error!')


@login_required
@csrf_exempt
# @user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def editRecord(request):
    if request.method == 'POST':

        id = request.POST["id"]
        customer = Client.objects.get(pk=id)
        try:
            description = request.POST["description"]
            customer.description = description
        except:
            pass

        try:
            title = request.POST["title"]
            customer.title = title
        except:
            pass

        try:
            certificate_type = request.POST["certificate_type"]
            customer.certificate_type = certificate_type
        except:
            pass

        try:
            certificate_name = request.POST["certificate_name"]
            customer.certificate_name = certificate_name
        except:
            pass

        try:
            ur = request.POST["ur"]
            customer.upload = ur
        except:
            pass

        try:
            uf = request.POST["uf"]
            customer.flookup_uploads = uf
        except:
            pass

        try:
            flookupdescription = request.POST["flookupdescription"]
            customer.flookup_description = flookupdescription
        except:
            pass

        customer.save()
    # Customer.objects.filter(pk=id).update(id = id, linkedin = linkedin, name = name, company = company,linkedin_title=designation,current_role=current_role,nature_of_work=nature_of_work_string,email = email,phone = phone,connection = connected_by,rating = rating, connect_type = connect_type_string, category=category_string, status=business_status, linkedin_summary=linkedin_summary)
    # print('-------------------')

    return redirect('/')


@login_required
@csrf_exempt
def upload(request):
    if request.method == "POST":
        try:
            id = request.POST["id"]
            customer = Client.objects.get(pk=id)
            amount = request.POST.get('amount')

            media_storage = MediaStorage()
            urls = ""
            show = []
            for k in range(int(amount)):
                ct = datetime.datetime.now()
                files = request.FILES.get("array"+str(k))
                url_name = files.name+"-"+str(ct)
                media_storage.save(url_name, files)
                show.append(url_name)
            if request.POST.get("section") == "client":
                print("client")
                if customer.upload == "N":
                    x = show

                else:

                    x = customer.upload.split(',')
                    x.append(show)

                response = {
                    'data': urls,
                    'data2': x,
                    "section": "client"
                }

            else:
                print("flookup")

                if customer.flookup_uploads == "N":
                    x = show

                else:

                    x = customer.flookup_uploads.split(',')
                    x.append(show)

                response = {
                    'data': urls,
                    'data2': x,
                    "section": "flookup"
                }

            return JsonResponse(response)

        except:
            print("failed to upload files")

    return redirect('/')


@login_required
@csrf_exempt
def new_upload(request):
    if request.method == "POST":
        try:
            amount = request.POST.get('amount')
            media_storage = MediaStorage()
            urls = ""
            show = []
            for k in range(int(amount)):
                ct = datetime.datetime.now()
                files = request.FILES.get("array"+str(k))
                url_name = files.name+"-"+str(ct)
                media_storage.save(url_name, files)
                show.append(url_name)

            response = {
                'data': urls,
                'data2': show
            }

            return JsonResponse(response)

        except:
            print("failed to upload in new record")

    return redirect('/')


@csrf_exempt
def open_files(request):
    if request.method == "POST":
        try:
            link = request.POST["link"]

            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'clientportalbucket',
                                                                'Key': 'Records/' + link},
                                                        ExpiresIn=200)

            return JsonResponse(response, safe=False)
        except:
            print("no such file available")

    # return redirect(response)


@csrf_exempt
def delete_files(request):
    if request.method == "POST":
        link = request.POST["link"]
        id = request.POST["id"]
        customer = Client.objects.get(pk=id)
        new_uploads = ""
        if request.POST["section"] == "client":
            print("client")
            uploads = customer.upload.split(',')

            for i in range(len(uploads)):
                if uploads[i] == link:
                    print('true')

                else:
                    new_uploads += ","+uploads[i]
                    print('false')
            if new_uploads:
                new_uploads = new_uploads[1:]
                customer.upload = new_uploads
                customer.save()
            else:
                new_uploads = "N"
                customer.upload = new_uploads
                customer.save()
        else:
            print("flookup")
            uploads = customer.flookup_uploads.split(',')
            print(uploads)
            for i in range(len(uploads)):
                if uploads[i] == link:
                    print('true')

                else:
                    new_uploads += ","+uploads[i]
                    print('false')
            if new_uploads:
                new_uploads = new_uploads[1:]
                customer.flookup_uploads = new_uploads
                customer.save()
            else:
                new_uploads = "N"
                customer.flookup_uploads = new_uploads
                customer.save()

        #     'Records/'+link

        response = s3_client.delete_object(
            Bucket='clientportalbucket',
            Key='Records/'+link,

        )
        r = {
            'data': new_uploads

        }

        return JsonResponse(r)

    return redirect("/")
