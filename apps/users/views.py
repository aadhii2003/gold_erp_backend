from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, UserLog
from apps.branches.models import Branch, UOM, Currency, Expense

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False)
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
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'branch', 'branch_name', 'last_login', 'is_active', 'password']

class UserLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserLog
        fields = '__all__'

class UserCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = self.request.user
        branch = serializer.validated_data.get('branch')
        if user.role == 'MANAGER':
            branch = user.branch
            
        # Extract password before saving
        password = serializer.validated_data.pop('password', None)
        new_user = serializer.save(branch=branch)
        
        if password:
            new_user.set_password(password)
            new_user.save()
        
        UserLog.objects.create(
            user=user,
            role=user.role,
            action="CREATE_USER",
            details=f"Created {new_user.role}: {new_user.username} for branch: {new_user.branch.name if new_user.branch else 'Global'}"
        )

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return User.objects.all()
        elif user.role == 'MANAGER':
            return User.objects.filter(branch=user.branch)
        return User.objects.none()

class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            
        UserLog.objects.create(
            user=self.request.user,
            role=self.request.user.role,
            action="UPDATE_USER",
            details=f"Updated user: {user.username} ({user.role})"
        )

class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Log before deletion
        UserLog.objects.create(
            user=self.request.user,
            role=self.request.user.role,
            action="DELETE_USER",
            details=f"Permanently removed user: {instance.username} ({instance.role})"
        )
        
        # Physical deletion
        self.perform_destroy(instance)
        return Response({'status': 'success', 'message': 'User deleted permanently'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

class UserStatusToggleView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        user_to_toggle = self.get_object()
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        
        UserLog.objects.create(
            user=request.user,
            role=request.user.role,
            action="TOGGLE_USER_STATUS",
            details=f"{'Enabled' if user_to_toggle.is_active else 'Disabled'} user: {user_to_toggle.username}"
        )
        return Response({'status': 'success', 'is_active': user_to_toggle.is_active})

class BranchCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer

    def perform_create(self, serializer):
        branch = serializer.save()
        UserLog.objects.create(
            user=self.request.user,
            role=self.request.user.role,
            action="CREATE_BRANCH",
            details=f"Established new branch: {branch.name} with X-Factor: {branch.x_factor}"
        )

class BranchListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer
    queryset = Branch.objects.all().order_by('-created_at')

class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()

    def perform_update(self, serializer):
        branch = serializer.save()
        UserLog.objects.create(
            user=self.request.user,
            role=self.request.user.role,
            action="UPDATE_BRANCH",
            details=f"Updated branch details for: {branch.name}"
        )

    def perform_destroy(self, instance):
        UserLog.objects.create(
            user=self.request.user,
            role=self.request.user.role,
            action="DELETE_BRANCH",
            details=f"Removed branch: {instance.name}"
        )
        instance.delete()

class UserLogListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogSerializer
    def get_queryset(self):
        # Allow Admin and Manager to view logs (can be filtered by role/branch in future if needed)
        return UserLog.objects.all().order_by('-created_at')

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
        expense = serializer.save(branch=branch)
        
        UserLog.objects.create(
            user=user,
            role=user.role,
            action="CREATE_EXPENSE",
            details=f"Recorded expense: {expense.grams}g @ {expense.rate_per_gram}/g for {expense.source_name}"
        )

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
