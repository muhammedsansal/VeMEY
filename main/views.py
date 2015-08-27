from django.shortcuts import render
from	django.contrib					import	messages
from	django.http						import	HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from	django.shortcuts				import	render_to_response, get_object_or_404, get_list_or_404
from	django.template					import	RequestContext
from	django.contrib.auth.decorators	import	login_required, user_passes_test
from	django.db.models				import	Q

# Create your views here.

@login_required
def home(request):

	variables = RequestContext( request , {} )

	return render_to_response('home.html' , variables )