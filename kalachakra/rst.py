from django.contrib.auth.models import User
User.objects.filter(is_superuser=True)
will list you all super users on the system. if you recognize yur username from the list:

usr = User.objects.get(username='admin')
usr.set_password('1')
usr.save()
