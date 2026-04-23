from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from apps.branches.models import Branch, UOM, Currency, Expense

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    class Meta:
        model = Expense
        fields = '__all__'

class UOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UOM
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'branch', 'branch_name', 'last_login', 'is_active']

class UserCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        user = self.request.user
        branch = serializer.validated_data.get('branch')
        if user.role == 'MANAGER':
            branch = user.branch
        new_user = serializer.save(branch=branch)
        password = self.request.data.get('password')
        if password:
            new_user.set_password(password)
            new_user.save()

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return User.objects.all().order_by('-id')
        elif user.role == 'MANAGER':
            return User.objects.filter(branch=user.branch).order_by('-id')
        return User.objects.none()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()

class BranchCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer

class BranchListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer
    queryset = Branch.objects.all().order_by('-created_at')

class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()

class UOMListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UOMSerializer
    queryset = UOM.objects.all()

class CurrencyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

class ExpenseCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    def perform_create(self, serializer):
        user = self.request.user
        branch = serializer.validated_data.get('branch')
        if user.role == 'MANAGER':
            branch = user.branch
        serializer.save(branch=branch)

class ExpenseListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Expense.objects.all().order_by('-date')
        elif user.role == 'MANAGER':
            return Expense.objects.filter(branch=user.branch).order_by('-date')
        return Expense.objects.none()
