from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializer import UserSerializer,UserProfileSerializer,SpamNumberSerializer,ContactSerializer
from.models import SpamNumber,Contact
from django.db.models import Q


User = get_user_model()
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'msg': 'Registration successful'})
    


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        print(password)
        print(phone_number)

        user = User.objects.filter(phone_number=phone_number).first()
        print(user,",,")
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid phone number or password'}, status=400)

        return Response({'msg': "Login succesfull"})




class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




class MarkSpamNumberView(generics.CreateAPIView):
    queryset = SpamNumber.objects.all()
    serializer_class = SpamNumberSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)





class SearchView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        user = self.request.user
        queryset = super().get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(name__startswith=query) | Q(name__contains=query) |
                Q(phone_number=query)
            )
        
        for contact in queryset:
            contact.spam_likelihood = self.calculate_spam_likelihood(contact.phone_number)
            contact.display_email = self.should_display_email(contact, user)
        
        return queryset
    
    def calculate_spam_likelihood(self, phone_number):
        try:
            spam_number = SpamNumber.objects.get(number=phone_number)
            return spam_number.number
        except SpamNumber.DoesNotExist:
            return 0
    
    def should_display_email(self, contact, user):
        if user.is_anonymous:
            return False
        elif user.contacts.filter(id=contact.id).exists():
            return True
        else:
            return False