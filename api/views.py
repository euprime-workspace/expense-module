from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from .serializers import *
from .models import *
from . import macros

@authentication_classes([])
@permission_classes([AllowAny])
class UserListCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            self.perform_create(serializer)
            return Response('Users created', status=status.HTTP_201_CREATED)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        self.perform_create(serializer)
        return Response('User Created', status=status.HTTP_201_CREATED)

# class ProjectListCreateView(generics.ListCreateAPIView):
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()

# class ItemListCreateView(generics.ListCreateAPIView):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()

# class ActionItemListCreateView(generics.ListCreateAPIView):
#     serializer_class = ActionItemSerializer
#     queryset = ActionItem.objects.all()

@authentication_classes([])
@permission_classes([AllowAny])
class ExpenseHeaderListCreateView(generics.ListCreateAPIView):
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

@authentication_classes([])
@permission_classes([AllowAny])
class ExtendedExpenseHeader(APIView):
    def get_object(self, UUID):
        try:
            return ExpenseHeader.objects.get(UUID=UUID)
        except ExpenseHeader.DoesNotExist:
            raise Http404

    def get_list(self, UUID):
        try:
            return ExpenseLine.objects.filter(expense_header_uuid=UUID)
        except ExpenseLine.DoesNotExist:
            return []

    def get(self, request, UUID):
        expense_header = self.get_object(UUID)
        expense_line =  self.get_list(UUID)
        serializerH = ExpenseHeaderSerializer(expense_header)
        serializerL = []
        for x in expense_line :
            serializerL.append(ExpenseLineSerializer(x).data)
        data = serializerH.data
        data["expense line"] = serializerL
        return Response(data)

@authentication_classes([])
@permission_classes([AllowAny])
class ExtendedExpenseHeaderAllUUID(APIView):
    def get_all_UUID(self):
        try:
            return ExpenseHeader.objects.values_list("UUID", flat=True)
        except ExpenseHeader.DoesNotExist:
            raise Http404
    def get_object(self, UUID):
        try:
            return ExpenseHeader.objects.get(UUID=UUID)
        except ExpenseHeader.DoesNotExist:
            raise Http404

    def get_list(self, UUID):
        try:
            return ExpenseLine.objects.filter(expense_header_uuid=UUID)
        except ExpenseLine.DoesNotExist:
            return []

    def get(self,request):
        output = []
        UUID_values = self.get_all_UUID()
        for UUID in UUID_values:
            expense_header = self.get_object(UUID)
            expense_line = self.get_list(UUID)
            serializerH = ExpenseHeaderSerializer(expense_header)
            serializerL = []
            for y in expense_line:
                serializerL.append(ExpenseLineSerializer(y).data)
            data = serializerH.data
            data["expense line"] = serializerL
            output.append(data)
        return Response(output)

    def get_list(self, UUID):
        try:
            return ExpenseLine.objects.filter(expense_header_uuid=UUID)
        except ExpenseLine.DoesNotExist:
            return []

    def get(self, request, UUID):
        expense_header = self.get_object(UUID)
        expense_line =  self.get_list(UUID)
        serializerH = ExpenseHeaderSerializer(expense_header)
        serializerL = []
        for x in expense_line :
            serializerL.append(ExpenseLineSerializer(x).data)
        data = serializerH.data
        data["expense line"] = serializerL
        return Response(data)

@authentication_classes([])
@permission_classes([AllowAny])
class ExtendedExpenseHeaderAllUUID(APIView):

    def get_all_UUID(self):
        try:
            return ExpenseHeader.objects.values_list("UUID", flat=True)
        except ExpenseHeader.DoesNotExist:
            raise Http404
    def get_object(self, UUID):
        try:
            return ExpenseHeader.objects.get(UUID=UUID)
        except ExpenseHeader.DoesNotExist:
            raise Http404

    def get_list(self, UUID):
        try:
            return ExpenseLine.objects.filter(expense_header_uuid=UUID)
        except ExpenseLine.DoesNotExist:
            return []

    def get(self,request):
        output = []
        UUID_values = self.get_all_UUID()
        for UUID in UUID_values:
            expense_header = self.get_object(UUID)
            expense_line = self.get_list(UUID)
            serializerH = ExpenseHeaderSerializer(expense_header)
            serializerL = []
            for y in expense_line:
                serializerL.append(ExpenseLineSerializer(y).data)
            data = serializerH.data
            data["expense line"] = serializerL
            output.append(data)
        return Response(output)

@authentication_classes([])
@permission_classes([AllowAny])
class ExpenseHeaderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
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
@authentication_classes([])
@permission_classes([AllowAny])
def expense_header_history(request, expense_header_uuid):
    historical_records = HistoricalExpenseHeader.objects.filter(UUID=expense_header_uuid)
    serializer = HistoricalExpenseHeaderSerializer(historical_records, many=True)
    return Response(serializer.data)

# GET,POST view of ExpenseLine
@authentication_classes([])
@permission_classes([AllowAny])
class ExpenseLineListCreateAPIView(generics.ListCreateAPIView):
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
@authentication_classes([])
@permission_classes([AllowAny])
class ExpenseLineRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer
    lookup_field = 'UUID'

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def expense_line_history(request, UUID):
    historical_records = HistoricalExpenseLine.objects.filter(UUID=UUID)
    serializer = HistoricalExpenseLineSerializer(historical_records, many=True)
    return Response(serializer.data)

@authentication_classes([])
@permission_classes([AllowAny])
class ExpenseLinesByExpenseHeader(generics.ListCreateAPIView):
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer

    def get_queryset(self):
        queryset = ExpenseLine.objects.all()
        expense_header_uuid = self.kwargs.get('expense_header_uuid')
        if expense_header_uuid:
            return get_list_or_404(ExpenseLine, expense_header_uuid=expense_header_uuid)
        else: raise Http404("expense_header_uuid not supplied")

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

@authentication_classes([])
@permission_classes([AllowAny])
class ExpenseLineByExpenseHeaderAndExpenseLineRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseLine.objects.all()
    serializer_class = ExpenseLineSerializer
    lookup_fields = ['UUID', 'expense_header_uuid']

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {}
        for lookup_field in self.lookup_fields:
            lookup_value = self.kwargs[lookup_field]
            filter_kwargs[lookup_field] = lookup_value
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj 

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def expense_lines_by_project_id(request):
    queryset = ExpenseLine.objects.all()
    project_id = request.query_params.get('project_id')
    if project_id:
        queryset = queryset.filter(project_id=project_id)
    action_item_id = request.query_params.get('action_item_id')
    if action_item_id:
        queryset = queryset.filter(action_item_id=action_item_id)
    status = request.query_params.get('status')
    if status:
        status = status.replace('"', '')
        queryset = queryset.filter(status=status)
    payment_status = request.query_params.get('payment_status')
    if payment_status:
        payment_status = payment_status.replace('"', '')
        queryset = queryset.filter(payment_status=payment_status)
    serializer = ExpenseLineSerializer(queryset, many=True)
    return Response(serializer.data)
