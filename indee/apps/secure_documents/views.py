from django.views.generic.base import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from apps.secure_documents.models import UserDocument

class UserLogin(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST['email']
            password = request.POST['password']
        except Exception:
            user = None
        else:
            user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('user_document')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')
            return redirect('login')


class UserDocuments(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDocuments, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        '''
        list old links and page to initate upload request
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        user_docs = UserDocument.objects.filter(user=request.user).order_by('-date_uploaded')
        return render(request, 'user_document.html', {'user_docs': user_docs[:10]})

    def post(self, request, *args, **kwargs):
        '''
        upload new document
        '''
        try:
            secure_link = True if request.POST.get('secure_link') else False
            file_to_save = request.FILES['selected_file']
        except Exception:
            messages.add_message(request, messages.ERROR, 'Invalid parameters!')
            return redirect('user_document')
        doc_type = file_to_save.name.split('.')[1].lower()
        if doc_type in ['pdf', 'txt']:
            doc_type = 0 if doc_type=='pdf' else 1
        else:
            messages.add_message(request, messages.ERROR, 'File not supported!')
            return redirect('user_document')
        user_doc = UserDocument.objects.create(user=request.user,
                                               doc_type=doc_type,
                                               doc=request.FILES['selected_file'])
        if secure_link:
            sec_hash = user_doc.generate_secure_link(save_to_inst=True)
        return redirect('user_document')


class SharedSecureDocument(View):


    def get(self, request, *args, **kwargs):
        '''
        view the document
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        sec_doc_id = kwargs['sec_doc_id']
        corres_doc = UserDocument.objects.filter(secure_link=sec_doc_id).first()
        if corres_doc:
            return render(request, 'doc_viewer.html', {'file_src': corres_doc.doc.url, 'file_type': corres_doc.doc_type,
                                                       't_file': corres_doc.doc.read()})
        else:
            raise Http404