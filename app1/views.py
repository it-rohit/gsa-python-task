from django.shortcuts import render
# from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import get_object_or_404




from .models import Task,User


from .serilizer import UserSerializer,TaskSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



#writingfunction creating token 



## registration module
class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user.username)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## 2 lgoin module 

class Login(APIView):

    def post(self, request):
        email = request.data.get('email')
        # print(email)
        password = request.data.get('password')
        print(password)

        # Check if both email and password are provided
        if not email or not password:
            
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Manually verify the password
        if user.check_password(password):
            # Login user
            login(request, user)
            return Response({"success": "Login successful"}, status=status.HTTP_200_OK)
        
        else:
            # Authentication failed
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)        

## add task
class TaskCreate(APIView):
   
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## view task
class TaskList(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # Fetch the user object or return 404 if not found
        tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, 'task_list.html', {'user': user, 'tasks': serializer.data})

