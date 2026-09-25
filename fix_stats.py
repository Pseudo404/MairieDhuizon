import re

with open("core/views.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define the new admin_stats function
new_admin_stats = """def admin_stats(request):
    if not user_is_panel_admin(request.user):
        return custom_403(request)

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    first_day_of_month = today_start.replace(day=1)

    if first_day_of_month.month == 1:
        first_day_prev_month = first_day_of_month.replace(year=first_day_of_month.year - 1, month=12)
    else:
        first_day_prev_month = first_day_of_month.replace(month=first_day_of_month.month - 1)

    views_today = PageView.objects.filter(created_at__gte=today_start, created_at__lt=today_end).count()
    views_month = PageView.objects.filter(created_at__gte=first_day_of_month).count()
    views_prev_month = PageView.objects.filter(
        created_at__gte=first_day_prev_month,
        created_at__lt=first_day_of_month
    ).count()

    unique_today = PageView.objects.filter(
        created_at__gte=today_start, created_at__lt=today_end
    ).values('session_key').distinct().count()
    unique_month = PageView.objects.filter(
        created_at__gte=first_day_of_month
    ).values('session_key').distinct().count()

    avg_time_result = PageView.objects.filter(
        time_on_page__isnull=False, time_on_page__gt=0, time_on_page__lt=3600,
    ).aggregate(avg=Avg('time_on_page'))
    avg_time = round(avg_time_result['avg'] or 0)

    if views_prev_month > 0:
        growth = round(((views_month - views_prev_month) / views_prev_month) * 100, 1)
    else:
        growth = 100.0 if views_month > 0 else 0.0

    thirty_days_ago = today_start - timedelta(days=29)
    # Optimization: do not group by Date in DB, do it in python if DB date is slow, but TruncDate is ok if indexed.
    # We will use TruncDate which is faster than __date
    from django.db.models.functions import TruncDate, TruncHour
    
    daily_views = (
        PageView.objects
        .filter(created_at__gte=thirty_days_ago)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    daily_data = {e['day']: e['count'] for e in daily_views if e['day']}

    daily_unique = (
        PageView.objects
        .filter(created_at__gte=thirty_days_ago)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('session_key', distinct=True))
        .order_by('day')
    )
    daily_unique_data = {e['day']: e['count'] for e in daily_unique if e['day']}

    chart_labels, chart_data, chart_unique_data = [], [], []
    for i in range(30):
        day = (thirty_days_ago + timedelta(days=i)).date()
        chart_labels.append(day.strftime('%d/%m'))
        chart_data.append(daily_data.get(day, 0))
        chart_unique_data.append(daily_unique_data.get(day, 0))

    hourly_views = (
        PageView.objects
        .filter(created_at__gte=today_start, created_at__lt=today_end)
        .annotate(hour=TruncHour('created_at'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('hour')
    )
    hourly_data = {}
    for e in hourly_views:
        h = e['hour']
        if h is not None:
            hourly_data[h.hour] = e['count']
    hourly_labels = [f'{h:02d}h' for h in range(24)]
    hourly_counts = [hourly_data.get(h, 0) for h in range(24)]

    top_pages = PageView.objects.values('path').annotate(count=Count('id')).order_by('-count')[:10]

    countries = [
        {'country': (e['country'] or 'Inconnu'), 'count': e['count']}
        for e in PageView.objects.values('country').annotate(count=Count('id')).order_by('-count')[:10]
    ]

    browsers = list(PageView.objects.exclude(browser='').values('browser').annotate(count=Count('id')).order_by('-count'))

    devices = list(PageView.objects.values('device_type').annotate(count=Count('id')).order_by('-count'))

    five_min_ago = now - timedelta(minutes=5)
    realtime_count = PageView.objects.filter(created_at__gte=five_min_ago).values('session_key').distinct().count()

    total_views = PageView.objects.count()

    app_views_today = PageView.objects.filter(created_at__gte=today_start, created_at__lt=today_end, path__startswith='/app/').count()
    app_views_month = PageView.objects.filter(created_at__gte=first_day_of_month, path__startswith='/app/').count()

    context = {"""

pattern = re.compile(r"def admin_stats\(request\):.*?context = \{", re.DOTALL)
new_content = pattern.sub(new_admin_stats, content)

with open("core/views.py", "w", encoding="utf-8") as f:
    f.write(new_content)
