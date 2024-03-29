from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.shortcuts import render

from func.user_manage import check_email

class UserPasswordResetView(PasswordResetView) : 
    template_name = 'user/password_reset.html'
    email_template_name = 'user/email/password_reset_email.html'
    subject_template_name = 'user/email/password_reset_subject.txt'

    def form_valid(self, form):
        if self.request.method == 'POST' :
            username = self.request.POST.get('username')
            email = self.request.POST.get('email')
            check = check_email(username, email)
            if check :
                opts = {
                    'use_https': self.request.is_secure(),
                    'token_generator': self.token_generator,
                    'from_email': self.from_email,
                    'email_template_name': self.email_template_name,
                    'subject_template_name': self.subject_template_name,
                    'request': self.request,
                    'html_email_template_name': self.html_email_template_name,
                    'extra_email_context': self.extra_email_context,
                }
                form.save(**opts)
                return super(PasswordResetView, self).form_valid(form)
            else :
                messages.error(self.request, '조회되지 않는 사용자입니다.')

        return render(self.request, 'user/password_reset.html')