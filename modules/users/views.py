from .models import Favorite, User, UserInterest, UserInterestPercent
from .forms import FavoriteForm, UserChangePassword
from django.views.generic.edit import UpdateView
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.middleware.csrf import get_token
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings 
import pdb
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

class FavAlterView(FormView):

    """
    Enables authenticated users to Favorite/Unfavorite objects.
    getattr method sets default values for POSITIVE_NOTATION, 
    NEGATIVE_NOTATION, ALLOW_ANONYMOUS in the case they are not
    set in settings.py
    """

    form_class = FavoriteForm
    model = Favorite
    template_name = 'fav/fav_form.html'

    def form_valid(self, form):
        fav_value = self.request.POST['fav_value']
        csrf_token_value = get_token(self.request)
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        try:
            content_type = ContentType.objects.get(app_label=self.request.POST['app_name'],model=self.request.POST['model'].lower())
            model_object = content_type.get_object_for_this_type(id=self.request.POST['model_id'])
            if fav_value == getattr(settings, 'POSITIVE_NOTATION', 'Favorite'):
                fav = form.save(commit=False)
                fav.content_object = model_object
                if self.request.user.is_authenticated:
                    fav.save()
                else:
                    if getattr(settings, 'ALLOW_ANONYMOUS', 'TRUE') == "TRUE":
                        fav.cookie = self.request.session.session_key
                        fav.save()
                    else:
                        return JsonResponse({
                            'success': 0,
                            'error': "You have to sign in "})
            else:
                if self.request.user.is_authenticated:
                    Favorite.objects.filter(
                        object_id=model_object.id,
                        user=self.request.user,
                        content_type=content_type).delete()
                elif getattr(settings, 'ALLOW_ANONYMOUS', 'TRUE') == "TRUE":
                    Favorite.objects.filter(
                        object_id=model_object.id,
                        cookie=self.request.session.session_key,
                        content_type=content_type).delete()
        except Exception as es:
            print(es)
            return JsonResponse({
                'success': 0,
                'error': "You have to sign in "})
        return JsonResponse({"csrf": csrf_token_value})

    def form_invalid(self, form):
        return JsonResponse({
            'success': 0,
            'error': form.errors})

class ProfileUpdate(UpdateView):
    model = User
    fields = ['username', 'email', 'profile_image','intrests',]
    template_name = 'dashboard/users/update.html'
    success_url = '/users/dashboard/profile'

    def get_context_data(self, **kwargs):
        data = super(ProfileUpdate, self).get_context_data(**kwargs)
        allInterest = UserInterest.objects.all()
        interestList = list(allInterest)
        allInterestPercent = UserInterestPercent.objects.filter(user = self.get_object())
        listInterestPercent = list(allInterestPercent)
        listInterest = []
        percentList = []
        for i in range(len(listInterestPercent)):
            percentList.append(listInterestPercent[i].percent)
            listInterest.append(listInterestPercent[i].interest.name)
        res = dict(zip(listInterest, percentList))
        if self.request.POST:
            data['interestList'] = listInterestPercent
            data['percentDict'] = res
            print(data['percentDict'])
        else:
            data['interestList'] = listInterestPercent
            data['percentDict'] = res
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form.save()
        listObj = []
        print('hello: ',context['percentDict'])
        for i in range( len(context['interestList'])):
            if context['percentDict'] != None:
                print(context['interestList'][i].id,'    ',self.request.POST.get('percent-{}'.format(i+1)))
                if context['interestList'][i].interest.name in [*context['percentDict'].keys()]:
                    a = UserInterestPercent.objects.filter(id = context['interestList'][i].id).update(percent = self.request.POST.get('percent-{}'.format(i+1)))
                    print(a)
                else:
                    listObj.append(UserInterestPercent(user = self.get_object(), interest = UserInterest.objects.get(name=self.request.POST.get('interest-{}'.format(i+1))),percent = self.request.POST.get('percent-{}'.format(i+1))))
            else:
                listObj.append(UserInterestPercent(user = self.get_object(), interest = UserInterest.objects.get(name=self.request.POST.get('interest-{}'.format(i+1))),percent = self.request.POST.get('percent-{}'.format(i+1))))
        UserInterestPercent.objects.bulk_create(listObj)
        return super(ProfileUpdate, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user

class ChangePasswordView(UpdateView):
    model = User
    form_class = UserChangePassword
    template_name = 'dashboard/users/change-password.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/users/dashboard/profile/')

    def get_object(self, queryset=None):
        return self.request.user

class ForgotPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home/forgot-password.html")

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email__iexact=request.POST.get('email'))
            context={
                'reset_password_url': '',
                'username': user.username
            }
            template = get_template('forgot-password-mail.html')
            html_string = template.render(context)
            self.sendMailes(html_string, user.email)
        except Exception as ex:
            print(ex)
        
        messages.info(request, 'You should get a forgot password link on your email address if your email is valid.')
        return HttpResponseRedirect('/')

    def sendMailes(self, html_string, receiver_email,**kwargs):
        try:
            from modules.site_settings.models import GeneralParams
            debug_mail = GeneralParams.objects.get(key="DEBUG_MAIL").value
            debug_email = GeneralParams.objects.get(key="DEBUG_SMTP_EMAIL").value
            smtp_password = GeneralParams.objects.get(key="SMTP_PASSWORD").value
            smtp_user = GeneralParams.objects.get(key="SMTP_USER").value
            smtp_host = GeneralParams.objects.get(key="SMTP_SERVER").value
            smtp_port = GeneralParams.objects.get(key="SMTP_PORT").value

            settings.EMAIL_HOST = smtp_host
            settings.EMAIL_HOST_USER = smtp_user
            settings.EMAIL_HOST_PASSWORD = smtp_password
            settings.EMAIL_PORT = int(smtp_port)
        except Exception as ex:
            print(ex)
            debug_mail = "0"

        if debug_mail == "1":
            receiver_email = debug_email

        try:
            subject = 'Reset password instruction.'
            email = EmailMessage(subject, html_string, settings.MAIL_FROM, [receiver_email])
            email.content_subtype = "html"
            email.send()
        except:
            pass


from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from io import StringIO, BytesIO


class CreateReportView(View):
    def get(self, request, *args, **kwargs):
        associate = User.objects.get(id=request.user.id).associate
        return render(request, "home/generate_report.html", {"associate":associate})

    def post(self, request, *args, **kwargs):
        range = request.POST.get("range").split(' - ')
        context = GetReportContext(range[0], range[1], request.user)
        file = GenerateReport(context)
        file.seek(0)
        response = HttpResponse(file,content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="download.docx"'
        return response


def GetReportContext(dt1, dt2, user):
    return {'fullname': user.first_name+' '+user.last_name}

def GenerateReport(context):
    template = DocxTemplate('LOG REPORT STRUCTURE.docx')
    target_file = BytesIO()
    template.render(context)
    template.save(target_file)
    return target_file