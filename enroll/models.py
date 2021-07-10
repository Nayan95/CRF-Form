from django.db import models
from django.forms import ModelForm

# Create your models here.


class Patient(models.Model):
	p_id = models.AutoField(primary_key=True,)
	f_name = models.CharField(max_length = 20)
	l_name = models.CharField(max_length = 20)
	age = models.IntegerField(default = 0)

	def __str__(self):
		return (self.f_name)


class Question(models.Model):
	q_id = models.IntegerField(primary_key = True)
	q_text = models.CharField(max_length = 500)

	def __str__(self):
		return self.q_text


class Result(models.Model):
	p_id = models.ForeignKey("Patient", on_delete=models.CASCADE, null=True)
	q_id = models.ForeignKey("Question", on_delete=models.CASCADE)
	ans_text = models.CharField(max_length=200)
	# ans_text = models.CharField(widget=models.RadioSelect, choices=truefalse)

	def __str__(self):
		return self.ans_text
