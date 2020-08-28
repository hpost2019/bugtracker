from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from custom_user.models import CustomUser
from homepage.models import Bugs
from homepage.forms import AddTicket, LoginForm


@login_required
def index(request):
    new_tickets = Bugs.objects.filter(status=Bugs.Status.NEW)
    in_prog_tickets = Bugs.objects.filter(status=Bugs.Status.IN_PROGRESS)
    done_tickets = Bugs.objects.filter(status=Bugs.Status.DONE)
    invalid_tickets = Bugs.objects.filter(status=Bugs.Status.INVALID)

    return render(
        request,
        "home.html",
        {
            "title": "Bug Tracker",
            "new_tickets": new_tickets,
            "in_prog_tickets": in_prog_tickets,
            "done_tickets": done_tickets,
            "invalid_tickets": invalid_tickets
        }
    )


@login_required
def ticket_view(request, ticket_id):
    data = Bugs.objects.filter(id=ticket_id).first()
    return render(
        request,
        "ticket_view.html",
        {
            "title": "Ticket View",
            "data": data
        }
    )


@login_required
def user_view(request, user_id):
    new_tickets = Bugs.objects.filter(
        status=Bugs.Status.NEW, filed_by=user_id)
    in_prog_tickets = Bugs.objects.filter(
        status=Bugs.Status.IN_PROGRESS, assigned_to=user_id)
    done_tickets = Bugs.objects.filter(
        status=Bugs.Status.DONE, completed_by=user_id)
    invalid_tickets = Bugs.objects.filter(
        status=Bugs.Status.INVALID, filed_by=user_id)
    user_info = CustomUser.objects.filter(id=user_id).first()

    return render(
        request,
        "user_view.html",
        {
            "title": "User Info",
            "new_tickets": new_tickets,
            "in_prog_tickets": in_prog_tickets,
            "done_tickets": done_tickets,
            "invalid_tickets": invalid_tickets,
            "user_info": user_info
        }
    )


@login_required
def add_ticket(request):
    if request.method == "POST":
        form = AddTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Bugs.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                filed_by=request.user
            )
            return HttpResponseRedirect(reverse('home'))
    form = AddTicket()
    return render(
        request,
        "generic_form.html",
        {
            "heading": "Add Ticket",
            "title": "Bug Tracker",
            "form": form
        }
    )


@login_required
def edit_ticket(request, ticket_id):
    ticket = Bugs.objects.get(id=ticket_id)
    if request.method == "POST":
        form = AddTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data.get('title')
            ticket.description = data.get('description')
            ticket.save()
            return HttpResponseRedirect(reverse('ticketV', args=[ticket.id]))
    data = {
        "title": ticket.title,
        "description": ticket.description
    }
    form = AddTicket(initial=data)
    return render(
        request,
        "generic_form.html",
        {
            "heading": "Edit Ticket",
            "title": "Bug Tracker",
            "form": form
        }
    )


@login_required
def assign_ticket(request, ticket_id):
    ticket = Bugs.objects.get(id=ticket_id)
    ticket.status = Bugs.Status.IN_PROGRESS
    ticket.assigned_to = request.user
    ticket.save()
    return HttpResponseRedirect(reverse('ticketV', args=[ticket.id]))


@login_required
def complete_ticket(request, ticket_id):
    ticket = Bugs.objects.get(id=ticket_id)
    ticket.status = Bugs.Status.DONE
    ticket.completed_by = request.user
    ticket.assigned_to = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticketV', args=[ticket.id]))


@login_required
def invalid_ticket(request, ticket_id):
    ticket = Bugs.objects.get(id=ticket_id)
    ticket.status = Bugs.Status.INVALID
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticketV', args=[ticket.id]))


@login_required
def return_ticket(request, ticket_id):
    ticket = Bugs.objects.get(id=ticket_id)
    ticket.status = Bugs.Status.NEW
    ticket.assigned_to = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticketV', args=[ticket.id]))


@login_required
def reopen_ticket(request, ticket_id):
    ticket = Bugs.objects.get(id=ticket_id)
    ticket.status = Bugs.Status.IN_PROGRESS
    ticket.assigned_to = request.user
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticketV', args=[ticket.id]))


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data.get("username"),
                password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('home')))
    form = LoginForm()
    return render(
        request,
        "generic_form.html",
        {
            'form': form,
            'title': 'Bug Tracker',
            'heading': 'Login required to use this app!'
        }
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
