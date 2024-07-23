from .models import *
from .serializers import *
from .services import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

# Create your views here.

# otp_token = data.get('otp_token', None)

class Set2FAView(APIView):

    def post(self, request):
        user = getUserService(request)
        if user is None:
            return JsonResponse({"status": "User id is invalid", "message": "No user with the corresponding user id exists"}, status=404)
        
        try:
            qr_code = getQRCodeService(user)
            return JsonResponse({"qr_code": qr_code})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class Verify2FAView(APIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()

	def post(self, request):
		"""
		Get the user, take the otp associated with them and verify it against the otp entered
		"""
		user = getUserService(request)
		if user == None:
			return Response({ "status": "Verification failed", "message": f"No user with the corresponding usern id exists"}, 
				status=status.HTTP_404_NOT_FOUND)

		valid_otp = getOTPValidityService(user, request.data.get('otp', None))
		if not valid_otp:
			return Response({ "status": "Verification failed", "message": "OTP is invalid or already used" }, 
				status=status.HTTP_400_BAD_REQUEST)
		return Response({ 'otp_verified': True })

class RegisterView(APIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()

	def post(self, request):
		"""
		Register View
		"""
		serializer = self.serializer_class(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({ "user_id": serializer.data['id'], "status": "Registration successful", "message": "Registered successfully, please login" }, 
				status=status.HTTP_201_CREATED)
		else:
			return Response({ "status": "Registration failed", "message": str(serializer.errors) }, 
				status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
	def post(self, request, *args, **kwargs):
		"""
		Login View
		"""
		user = getLoginUserService(request)
		if user == None:
			return Response({
				"status": "Login failed", 
				"message": f"No user with the corresponding username and password exists"
				}, 
				status=status.HTTP_404_NOT_FOUND)
		return Response({ 'user_id': user.id })

@api_view(['POST'])
def isLoggedIn(request):
	"""
	Check if user is logged in
	"""
	user = getUserService(request)
	if user == None:
		return Response({ "user_null": True }, status=status.HTTP_404_NOT_FOUND)
	elif user.logged_in == True:
		return Response({ "logged_in": True }, status=status.HTTP_404_NOT_FOUND)
	return Response({ 'user_id': user.id })