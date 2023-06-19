import random
import string
from faker import Faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from  .models import Contact, SpamNumber

fake = Faker()

# To use this script, save it as a Python file (e.g:data_population_script.py) and run the following command:
# This script uses the Faker library to generate random data for user names, email addresses, phone numbers, etc. 
# It creates a specified number of users, contacts, and spam numbers using the create_users, create_contacts,
# and create_spam_numbers methods, respectively.
# installation : pip install Faker


class Command(BaseCommand):
    # the script will display the provided message as the help text when executing the,
    # python manage.py populate_data --help command.
    help = 'Populate the database with random sample data.'

    def handle(self, *args, **options):
        self.create_users(10)
        self.create_contacts(50)
        self.create_spam_numbers(20)

    def create_users(self, num_users):
        for _ in range(num_users):
            username = fake.user_name()
            email = fake.email()
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            User.objects.create_user(username=username, email=email, password=password)

    def create_contacts(self, num_contacts):
        users = User.objects.all()
        for _ in range(num_contacts):
            name = fake.name()
            phone_number = fake.phone_number()
            user = random.choice(users)
            Contact.objects.create(name=name, phone_number=phone_number, user=user)

    def create_spam_numbers(self, num_spam_numbers):
        for _ in range(num_spam_numbers):
            number = fake.phone_number()
            likelihood = random.randint(1, 10)
            SpamNumber.objects.create(number=number, likelihood=likelihood)

