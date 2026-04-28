from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, serializers
from .models import Sale
from apps.branches.models import Branch
from apps.users.models import UserLog

class SaleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.username', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    class Meta:
        model = Sale
        fields = '__all__'

class SalesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Sale.objects.all().order_by('-created_at')
        elif user.role == 'MANAGER':
            return Sale.objects.filter(branch_id=user.branch_id).order_by('-created_at')
        else:
            return Sale.objects.filter(staff=user).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_sales(request):
    data = request.data
    sales = data.get('sales', [])
    created_count = 0
    errors = []
    
    # Staff's branch
    branch_id = request.user.branch_id
    
    for s in sales:
        try:
            if not Sale.objects.filter(id=s['id']).exists():
                products = s.get('products', [])
                p = products[0] if len(products) > 0 else {}

                Sale.objects.create(
                    id=s['id'],
                    branch_id=branch_id,
                    staff=request.user,
                    
                    # RFQ
                    vendor=s.get('client_name') or s.get('vendor'),
                    purchase_method=s.get('purchase_method', ''),
                    market_price_currency=s.get('market_currency', 'USD'),
                    market_price=s.get('market_price', 0),
                    discount_addition=s.get('discount_additions', 0),
                    net_price=s.get('net_price', 0),
                    market_price_unit=s.get('material_unit', 'g'),
                    
                    # Header / Constants
                    order_deadline=s.get('filing_date') or s.get('order_deadline'),
                    expected_arrival=s.get('expected_arrival'),
                    transaction_currency=s.get('change_currency', 'USD'),
                    currency_rate=s.get('change_currency_rate', 1.0),
                    transaction_unit=s.get('transaction_unit', 't'),
                    conversion_market_unit=s.get('conversion_market_unit', 0.38),
                    x_factor=s.get('x_factor', 92.0),
                    payment_ref=s.get('payment_ref', 'Paid Unfixed Amount'),
                    paid_amount=s.get('paid_amount', 0),
                    balance=s.get('balance', 0),

                    # Product
                    product_name=p.get('productName', 'Gold Bar'),
                    description=p.get('description', ''),
                    gross_weight=p.get('grossWeight', 0) if p.get('grossWeight') not in ('', None) else 0,
                    actual_process_weight=p.get('actualProcessWeight', 0) if p.get('actualProcessWeight') not in ('', None) else 0,
                    second_process_weight=p.get('secondProcessWeight', 0) if p.get('secondProcessWeight') not in ('', None) else 0,
                    process_loss=p.get('processLoss', 0),
                    density=p.get('density', 0),
                    actual_product_quality=p.get('finalPurity', 0),
                    
                    manual_first_process=p.get('manualFirstProcess', 0) if p.get('manualFirstProcess') not in ('', None) else 0,
                    manual_purity=p.get('manualPurity', 0) if p.get('manualPurity') not in ('', None) else 0,
                    qty_tolas=p.get('tolaQty', 0),
                    tola_rate=s.get('tola_rate', 0),

                    unit_price=p.get('unitPrice', 0),
                    subtotal=s.get('subtotal', 0),
                    total_ugx=s.get('total_target_currency', 0)
                )
                created_count += 1
                
                UserLog.objects.create(
                    user=request.user,
                    role=request.user.role,
                    action="CREATE_SALE",
                    details=f"Processed transaction {s['id']} for {s.get('vendor', 'Unknown')} (Total: {s.get('subtotal', 0)} USD)"
                )
        except Exception as e:
            errors.append({'id': s.get('id'), 'error': str(e)})

    return Response({"status": "success", "synced_count": created_count, "errors": errors})
