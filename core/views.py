from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import TaskManager, DailyTask, ExpenseTracker, DailyTaskLog
from django.db.models import Sum
from django.db.models.functions import TruncDate
import json
from django.utils import timezone
from datetime import timedelta

def home(request):
    today = timezone.now().date()
    
    # Get today's incomplete tasks
    todays_tasks = DailyTaskLog.objects.filter(
        date=today,
        completed=False
    ).select_related('task')
    
    # Get pending tasks from task manager
    pending_tasks = TaskManager.objects.filter(completed_at__isnull=True).order_by('-id')
    
    # Task Graph Data (last 30 days)
    start_date = today - timedelta(days=30)
    tasks = DailyTask.objects.all()
    
    graph_dates = []
    completed_counts = []
    
    for i in range(31):
        day = start_date + timedelta(days=i)
        completed = DailyTaskLog.objects.filter(
            date=day,
            completed=True
        ).count()
        graph_dates.append(str(day))
        completed_counts.append(completed)
    
    total_tasks = tasks.count()
    
    # Expense Graph Data
    expenses_data = (
        ExpenseTracker.objects
        .annotate(day=TruncDate('date'))   
        .values('day')
        .annotate(total=Sum('amount'))
        .order_by('day')
    )
    
    expense_dates = json.dumps([str(item['day']) for item in expenses_data])
    expense_totals = json.dumps([float(item['total']) for item in expenses_data])
    
    return render(request, 'home.html', {
        'todays_tasks': todays_tasks,
        'pending_tasks': pending_tasks,
        'graph_dates': json.dumps(graph_dates),
        'completed_counts': json.dumps(completed_counts),
        'total_tasks': total_tasks,
        'expense_dates': expense_dates,
        'expense_totals': expense_totals
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def dailytask(request):
    today = timezone.now().date()

    if request.method == 'POST' and 'title' in request.POST:
        title = request.POST.get('title')
        if title:
            DailyTask.objects.create(title=title)
        return redirect('dailytask')

    tasks = DailyTask.objects.all()
    for task in tasks:
        DailyTaskLog.objects.get_or_create(task=task, date=today)

    todays_tasks = DailyTaskLog.objects.filter(
        date=today,
        completed=False
    ).select_related('task')

    all_logs = DailyTaskLog.objects.all().order_by('-date')
    today = timezone.now().date()
    start_date = today - timedelta(days=30)

    tasks = DailyTask.objects.all()

    performance_data = {}

    for task in tasks:
        logs = DailyTaskLog.objects.filter(
            task=task,
            date__range=(start_date, today)
        )

        log_dict = {log.date: log.completed for log in logs}

        days = []
        for i in range(31):
            day = start_date + timedelta(days=i)
            days.append({
                "date": day,
                "completed": log_dict.get(day, False)
            })

        performance_data[task.id] = days

    # Task Graph Data
    graph_dates = []
    completed_counts = []
    
    for i in range(31):
        day = start_date + timedelta(days=i)
        completed = DailyTaskLog.objects.filter(
            date=day,
            completed=True
        ).count()
        graph_dates.append(str(day))
        completed_counts.append(completed)
    
    total_tasks = tasks.count()

    return render(request, 'daily_task.html', {
        'todays_tasks': todays_tasks,
        'tasks': tasks,
        'performance_data': performance_data,
        'graph_dates': json.dumps(graph_dates),
        'completed_counts': json.dumps(completed_counts),
        'total_tasks': total_tasks
    })


def complete_task(request, task_id):
    today = timezone.now().date()
    print(f"Completing task {task_id} for date {today}")

    try:
        log, created = DailyTaskLog.objects.get_or_create(task_id=task_id, date=today)
        log.completed = True
        log.save()
        print(f"Task completed: {log}")
    except Exception as e:
        print(f"Error completing task: {e}")

    return redirect('dailytask')

def update_daily_task(request, task_id):
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        if new_title:
            task = DailyTask.objects.get(id=task_id)
            task.title = new_title
            task.save()
        return redirect('dailytask')
    
    task = DailyTask.objects.get(id=task_id)
    return render(request, 'daily_task.html', {'edit_task': task})

def delete_daily_task(request, task_id):
    DailyTask.objects.filter(id=task_id).delete()
    return redirect('dailytask')

def expensetracker(request):

    if request.method == 'POST' and 'amount' in request.POST:
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')

        ExpenseTracker.objects.create(
            amount=amount,
            reason=reason
        )
        return redirect('expensetracker')

    expenses = ExpenseTracker.objects.all().order_by('-id')

    data = (
        ExpenseTracker.objects
        .annotate(day=TruncDate('date'))   
        .values('day')
        .annotate(total=Sum('amount'))
        .order_by('day')
    )

    dates = json.dumps([str(item['day']) for item in data])
    totals = json.dumps([float(item['total']) for item in data])

    return render(request, 'expense_tracker.html', {
        'expenses': expenses,
        'expenses_all': expenses,
        'dates': dates,
        'totals': totals
    })

def update_expense(request, expense_id):
    if request.method == 'POST':
        new_amount = request.POST.get('new_amount')
        new_reason = request.POST.get('new_reason')
        if new_amount:
            exp = ExpenseTracker.objects.get(id=expense_id)
            exp.amount = new_amount
            exp.reason = new_reason
            exp.save()
        return redirect('expensetracker')
    exp = ExpenseTracker.objects.get(id=expense_id)
    return render(request, 'expense_tracker.html', {'edit_expense': exp})

def delete_expense(request, expense_id):
    ExpenseTracker.objects.filter(id=expense_id).delete()
    return redirect('expensetracker')
def taskmanager(request):
    if request.method == 'POST' and 'task_name' in request.POST:
        task_name = request.POST.get('task_name')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        if task_name:
            TaskManager.objects.create(
                title=task_name,
                priority=priority,
                deadline=deadline
            )

        return redirect('taskmanager')

    tasks = TaskManager.objects.filter(completed_at__isnull=False).order_by('-id')
    tasks_pending = TaskManager.objects.filter(completed_at__isnull=True).order_by('-id')
    tasks_all = TaskManager.objects.all().order_by('-id')

    return render(request, 'task_manager.html', {
        'tasks': tasks,
        'tasks_pending': tasks_pending,
        'tasks_all': tasks_all,
    })
def complete_taskmanager(request, task_id):
    task = TaskManager.objects.get(id=task_id)
    task.completed_at = timezone.now()
    task.save()

    return redirect('taskmanager')

def update_taskmanager(request, task_id):
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        new_priority = request.POST.get('new_priority')
        new_deadline = request.POST.get('new_deadline')
        
        if new_title:
            task = TaskManager.objects.get(id=task_id)
            task.title = new_title
            task.priority = new_priority
            task.deadline = new_deadline
            task.save()
        return redirect('taskmanager')
    
    task = TaskManager.objects.get(id=task_id)
    return render(request, 'task_manager.html', {'edit_task': task})

def delete_taskmanager(request, task_id):
    TaskManager.objects.filter(id=task_id).delete()
    return redirect('taskmanager')
