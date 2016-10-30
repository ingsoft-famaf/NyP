"""
Views for app chm
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from allauth.account.views import login

from chm.models import Question, QuestionOnQuiz, Answer, Flag
from chm.forms import QuizForm, FlagForm
from chm.forms import Quiz

def index(request):
    """
    If the user is authenticated redirect to login, otherwise display index
    page.
    """

    if not request.user.is_authenticated:
        return redirect(login)
    else:
        context = {}
        if request.user.is_staff:
            nfq = Question.objects.filter(flags__isnull=False).count()
            context['n_flagged_questions'] = nfq
    return render(request, 'index.html', context)


@login_required
def new_quiz(request):
    """ User wants to start an exam."""

    if request.method == 'POST':
        form = QuizForm(request.POST, user=request.user)
        if form.is_valid():
            quiz = form.make_quiz()
            return render(request, 'quiz.html', {'quiz': quiz.to_json()})
    else:
        form = QuizForm()

    return render(request, 'new_quiz.html', {'form': form})


def correct_quiz(request):
    """ Verify user answers"""

    if request.method == 'POST':
        quiz_id = request.POST('quiz_id')

        # fail with 404 if quiz doesn't exist
        quiz = get_object_or_404(pk=quiz_id)

        # fail with 403 if user didn't take this quiz
        if request.user != quiz.user:
            raise PermissionDenied

        for answer in request.POST('answer'):
            qoq = QuestionOnQuiz.objects.get(
                question_id=answer['question_id'],
                quiz_id=quiz_id
            )
            correct_answers_ids = Answer.objects.filter(
                question=answer['question_id'],
                is_correct=True
            ).values('pk')

            if not answer['answer_id']:
                # user didn't choose any answer
                qoq.state = QuestionOnQuiz.STATUS.not_answered
            if set(answer['answer_id']) == set(correct_answers_ids):
                qoq.state = QuestionOnQuiz.STATUS.right
            else:
                qoq.state = QuestionOnQuiz.STATUS.wrong
            qoq.save()

        return render(request, 'quiz_results.html', {'quiz': quiz})
    else:
        return render(request, 'index.html')


def timer(request):
    seconds = request.GET.get('seconds', 10)
    return render(request, 'timer.html', {'seconds': seconds})


def flag_question(request, id):
    question = get_object_or_404(Question, id=id)
    context = {'question': question}
    if request.method == 'POST':
        form = FlagForm(request.POST)
        if form.is_valid():
            flag = Flag.objects.create(
                question=question,
                user=request.user,
                description=form.cleaned_data['description'],
            )
            context['flag'] = flag
    else:
        form = FlagForm()

    context['form'] = form
    return render(request, 'flag.html', context)
