import json
from collections import Counter
from .anomaly_detection import detect_anomalies  # import your function
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from dashboard.forms import FoodItemForm
# Create your views here.
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .anomaly_detection import detect_anomalies
from django.contrib.auth.decorators import login_required
from dashboard.models import FoodItem, Monitoring


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def report_upload(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            df = detect_anomalies(file_path=file_path)
            html_table = df.to_html(
                classes='table table-bordered', index=False)

            # Count anomalies vs normal
            anomaly_counts = dict(Counter(df['Anomaly']))
            anomaly_labels = list(anomaly_counts.keys())
            anomaly_values = list(anomaly_counts.values())

            return render(request, 'dashboard/report_result.html', {
                'table': html_table,
                'labels': json.dumps(anomaly_labels),
                'values': json.dumps(anomaly_values)
            })

        except Exception as e:
            return render(request, 'dashboard/report_upload.html', {'error': str(e)})

    return render(request, 'dashboard/report_upload.html')


@login_required
def create_shipment(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user
            food_item.save()

            # Automatically create Monitoring entry
            Monitoring.objects.create(
                food_item=food_item,
                driver=request.user,
                current_temperature=food_item.temperature,
                current_humidity=food_item.humidity,
                current_location=food_item.location,
                status='Safe'
            )

            return redirect('dashboard')
    else:
        form = FoodItemForm()

    return render(request, 'dashboard/create_shipment.html', {'form': form})

@login_required
def track_deliveries(request):
    user = request.user
    print(user)
    food_items = FoodItem.objects.filter(user=user)
    print(food_items)
    if not food_items:
        active_deliveries = []
    else:
        active_deliveries = Monitoring.objects.filter(
            food_item__in=food_items).order_by('-timestamp')
        print(active_deliveries)
    return render(request, 'dashboard/track_deliveries.html', {'deliveries': active_deliveries})
