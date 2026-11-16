from django.contrib.auth.views import LoginView


class StaffLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
