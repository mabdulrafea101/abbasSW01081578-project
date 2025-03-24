from django.contrib.auth.mixins import UserPassesTestMixin


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'manager'


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'teacher'


class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'student'

