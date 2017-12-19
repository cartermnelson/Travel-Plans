# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
import bcrypt

def index(request): #GET
	return redirect("/main")

def main(request):
	if request.session.get("user_id"):
		return redirect("/travels")
	else:
		return render(request, "travel/index.html")

def register(request): #POST
	if request.method == 'POST':
		errors = User.objects.validate_register(request.POST)
		if errors:
			for error in errors:
				messages.error(request, error)
			return redirect("/main")
		else:
			User.objects.add_user(request.POST)
			request.session['user_id'] = User.objects.get(email = request.POST["email"]).id
			return redirect("/success")

	else:
		return redirect("/main")

def login(request): #POST
	errors = User.objects.validate_login(request.POST)
	if type(errors) == list:
		for error in errors:
			messages.error(request, error)
		return redirect("/main")
	else:
		request.session['user_id'] = errors.id
		return redirect("/travels")

def logout(request): #POST
	request.session.clear()
	return redirect("/main")

def success(request): #GET
	if request.session.get('user_id'):
		context = {
			"user": User.objects.get(id=request.session.get('user_id'))
		}
		return render(request, "travel/success.html", context)
	else:
		return redirect("/main")

def travels(request): #GET
	if request.session.get('user_id'):
		context = {
			"users": User.objects.all(),
			"plans": Travel.objects.all(),
			"user": User.objects.get(id = request.session.get('user_id')),
			"trips_joined": User.objects.get(id = request.session.get('user_id')).trips_joined.all(),
		}
		return render(request, "travel/travels.html", context)
	else:
		return redirect("/main")

def add(request): #GET
	return render(request, "travel/add.html")

def addPlan(request): #POST
	if request.method=='POST':
		errors = Travel.objects.validate_destination(request.POST)
		if errors:
			for error in errors:
				messages.error(request, error)
			return redirect("/travels/add")
		else:
			Travel.objects.add_destination(request.POST, request.session.get('user_id'))
			return redirect("/travels")

	else:
		return redirect("/main")

def destination(request, id): #GET
	if Travel.objects.filter(id = id):
		context = {
			"dest": Travel.objects.get(id = id),
			"joined": Travel.objects.get(id = id).users_joined.all(),
		}
		return render(request, "travel/destination.html", context)
	else:
		return redirect("/travels")

def joinDestination(request, id): #POST
	Travel.objects.join_destination(id, request.session.get('user_id'))
	return redirect("/travels")
