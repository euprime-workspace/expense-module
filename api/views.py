from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.decorators import authentication_classes, permission_classes
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated

class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
@permission_classes([IsAuthenticated])
class ProjectListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
@permission_classes([IsAuthenticated])
class ItemListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

@permission_classes([IsAuthenticated])
#@authentication_classes((JWTAuthentication))
class ActionItemListCreateView(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ActionItemSerializer
    queryset = ActionItem.objects.all()

@permission_classes([IsAuthenticated])
class ExpenseHeaderListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ExpenseHeaderSerializer

    # overiding the default get_queryset function
    def get_queryset(self):
        # Get the project_id parameter from the query string
        project_id = self.request.query_params.get('project_id')

        # Filter the queryset based on project_id
        queryset = ExpenseHeader.objects.all()

        if project_id:
            queryset = queryset.filter(
                ExpenseLine_expense_header__project_id=project_id)  # filter qs according to project_id

        return queryset

    # overiding default create method
    def create(self, request, *args, **kwargs):
        # Get the change_reason from the request data or as a query parameter
        change_reason = request.data.get('change_reason')
        # print("reasonview: ", change_reason)

        # Check if the request data is a list
        if isinstance(request.data, list):
            # Serialize each object in the list and save them
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, change_reason=change_reason)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If not a list, proceed with creating a single object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, change_reason=change_reason)  # Pass change_reason as kwargs
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # overriding default perform_create
    def perform_create(self, serializer, change_reason=None):
        # Get the current user
        # print("Vchange_reason: ",change_reason)
        user = User.objects.first()  # TODO: Evaluate current authenticated user

        # If request data is a list
        if isinstance(serializer.validated_data, list):
            # Create each object with the user as the creator and updator
            for obj in serializer.validated_data:
                obj['created_by'] = user
                obj['updated_by'] = user
                obj['change_reason'] = change_reason  # Set the change_reason for each object
            serializer.save()
        else:
            # For a single object, set the change_reason and other fields
            validated_data = serializer.validated_data
            validated_data['created_by'] = user
            validated_data['updated_by'] = user
            validated_data['change_reason'] = change_reason  # Set the change_reason
            serializer.save(**validated_data)

@permission_classes([IsAuthenticated])
class ExpenseHeaderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = ExpenseHeader.objects.all()
    serializer_class = ExpenseHeaderSerializer
    lookup_field = 'UUID'

    def delete(self, request, *args, **kwargs):
        # Generate the deleted_by data, for example, from the request user
        deleted_by = User.objects.first()  # TODO: Evaluate current authenticated user to use as deleted_by
        # Call the serializer's delete method and pass deleted_by as a keyword argument
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.delete(instance, deleted_by=deleted_by)  # Pass deleted_by as a keyword argument

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_header_history(request, UUID):
    
    # Get the Expense_header instance
    expense_header = get_object_or_404(ExpenseHeader, UUID=UUID)

    # Get the historical records for the Expense_header
    historical_records = HistoricalExpense_headers.objects.filter(
        UUID=expense_header.UUID,  # Assuming you have an id field for ExpenseHeader
    )

    # Serialize the historical records
    serializer = HistoricalExpenseHeadersSerializer(historical_records, many=True)

    return Response(serializer.data)

# GET,POST view of ExpenseLine
@permission_classes([IsAuthenticated])
class ExpenseLineListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer

    # overiding default post method
    def post(self, request, *args, **kwargs):
        data = request.data
        # if request data is a list
        if isinstance(data, list):
            serializer = ExpenseLineSerializer(data=data, many=True)
        else:
            serializer = ExpenseLineSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # overiding default get_queryset method
    def get_queryset(self):
        # filtering according to endpoint
        action_item_id = self.request.query_params.get('action_item_id')
        status = self.request.query_params.get('status')
        payment_status = self.request.query_params.get('payment_status')

        queryset = ExpenseLine.objects.all()

        if action_item_id:
            queryset = queryset.filter(action_item_id=action_item_id)

        if status:
            queryset = queryset.filter(status=status)

        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        return queryset


# GET,PATCH,PUT,DESTROY view of expense_line(with givien UUID)
@permission_classes([IsAuthenticated])
class ExpenseLineRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer
    lookup_field = 'UUID'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_line_history(request, UUID):
    authentication_classes = [JWTAuthentication]
    expense_line = get_object_or_404(ExpenseLine, UUID=UUID)

    his = HistoricalExpenseLine.objects.filter(
        UUID=expense_line.UUID,
    )

    serializer = HistoricalExpenseLineSerializer(his, many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
class ExpenseLinesByExpenseHeader(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer

    def get_queryset(self):
        queryset = ExpenseLine.objects.all()
        header_id = self.request.query_params.get('header_id')
        if header_id:
            queryset.filter(expense_header_id=header_id)
        line_id = self.request.query_params.get('line_id')
        if line_id:
            queryset.filter(UUID=line_id)
        return queryset

    def post(self, request, *args, **kwargs):
        data = request.data
        # if request data is a list
        if isinstance(data, list):
            serializer = ExpenseLineSerializer(data=data, many=True)
        else:
            serializer = ExpenseLineSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class ExpenseLineByExpenseHeaderAndExpenseLineListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer
    lookup_field = 'UUID'

    def get_queryset(self):
        queryset = ExpenseLine.objects.all()
        line_id = self.request.query_params.get('line_id')
        if line_id:
            queryset.filter(UUID=line_id)
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
@permission_classes([IsAuthenticated])
class ExpenseLineByExpenseHeaderAndExpenseLineRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer
    lookup_field = 'UUID'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
