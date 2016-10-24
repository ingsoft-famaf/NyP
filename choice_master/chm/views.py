from django.shortcuts import render
from django.shortcuts import redirect
from allauth.account.views import login
from django.contrib import messages

from lxml.etree import XMLSyntaxError
from chm.forms import XMLFileForm
from chm.models import Topic
from chm.xml import parse_questions

from chm import similarity


def index(request):
    """
        If the user is authenticated redirect to login, otherwise display index
    """
    if not request.user.is_authenticated:
        return redirect(login)
    return render(request, 'index.html')


def extract_topic_and_subject_from_data(data):
    topic_and_subject = str(data['topic'])
    subject = ' (' + str(data['subject']) + ')'
    topic = topic.replace(subject, '')
    return topic, subject


def upload(request):
    context = {'added': [],
               'repeated': [],
               'similar_exists': []}

    if request.method == 'POST':
        form = XMLFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            try:
                xmlfile = request.FILES['XMLfile']
                for question, answers in parse_questions(xmlfile):
                    topic, subject = extract_topic_and_subject_from_data(data)
                    question.topic = Topic.objects.get(name=topic)

                    if similarity.repeated(question):
                        context['repeated'].append(question)
                    elif similarity.similar_exists(question):
                        context['similar_exists'].append(question)
                    else:
                        context['added'].append(question)

                        question.save()
                        for ans in answers:
                            ans.question = question
                            ans.save()

            except XMLSyntaxError as err:
                context['syntax_error'] = err
    else:
        form = XMLFileForm()

    context['form'] = form
    # Load documents for the list page
    return render(request, 'upload.html', context)
