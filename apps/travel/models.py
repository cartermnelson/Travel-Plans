# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# (r'^[a-zA-Z\']+')

class UserManager(models.Manager):
	def validate_register(self, postData):
		errors = []

		#Check for blank forms
		if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['password']) < 1:
			errors.append("Please complete all fields")
		else:
			#Check if first and last name have at least 2 characters
			if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
				errors.append("First and last name should be more than 2 characters")
			#Check if first or last name have non-letter characters
			elif not postData["first_name"].isalpha() or not postData["first_name"].isalpha():
				errors.append("First or last name contains invalid characters")

			#Check email format
			if not EMAIL_REGEX.match(postData["email"]):
				errors.append("Invalid email address")

			#Check if password contains at least 8 characters
			if len(postData['password']) < 8:
				errors.append("Password must contain at least 8 characters")
			#Check if password matches confirmation
			elif postData["password"] != postData["cpassword"]:
				errors.append("Passwords do not match")

			#Check if email exists
			if not errors and self.filter(email=postData['email']):
				errors.append("Email already registered")

		return errors

	def add_user(self, postData):
		hash = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
		print hash
		self.create(
			first_name = postData["first_name"],
			last_name = postData["last_name"],
			email = postData["email"].lower(),
			password = hash
		)

	def validate_login(self, postData):
		errors = []
		users = self.filter(email=postData['email'].lower())
		if users:
			user = users[0]
			if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				errors.append('email/password incorrect')

			if errors:
				return errors
			return user
		else:
			errors.append('email/password incorrect')
			return errors

class User(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()


class TravelManager(models.Manager):
	def validate_destination(self, postData):
		errors = []

		#Check for empty forms
		if len(postData['dest']) < 1 or len(postData['desc']) < 1 or len(postData['date_from']) < 1 or len(postData['date_to']) < 1:
			errors.append("Please complete all fields")
		else:
			#Check if dates are future-dated
			print postData["date_from"]
			print date.today()
			if postData["date_from"] < unicode(str(date.today()), "utf-8") or postData["date_to"] < unicode(str(date.today()), "utf-8"): 
				errors.append("Dates must be today or in the future")

			#Check if start date is after end date
			if postData["date_to"] < postData["date_from"]:
				errors.append("Start date must be before end date")

		return errors

	def add_destination(self, postData, user_id):
		Travel.objects.create(
		dest = postData["dest"],
		desc = postData["desc"],
		date_from = postData["date_from"],
		date_to = postData["date_to"],
		planner = User.objects.get(id = user_id)
		)

	def join_destination(self, dest_id, user_id):
		if not self.get(id = dest_id).users_joined.filter(id = user_id) and self.get(id = dest_id).planner.id != user_id:
			self.get(id = dest_id).users_joined.add(User.objects.get(id = user_id))
		else:
			print "can't join twice/join own trip"

class Travel(models.Model):
	dest = models.CharField(max_length = 255)
	desc = models.TextField()
	date_from = models.DateField()
	date_to = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	planner = models.ForeignKey(User, related_name = "plans")
	users_joined = models.ManyToManyField(User, related_name = "trips_joined")

	objects = TravelManager()