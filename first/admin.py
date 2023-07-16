# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Expense, Income, Token, News
# Register your models here.

admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Token)
admin.site.register(News)