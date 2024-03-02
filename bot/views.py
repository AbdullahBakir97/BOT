from django.shortcuts import render, redirect
from .models import Bot

def index(request):
    """
    View function to display a list of bots.
    """
    bots = Bot.objects.all()
    return render(request, 'index.html', {'bots': bots})

def bot_detail(request, bot_id):
    """
    View function to display details of a specific bot.
    """
    bot = Bot.objects.get(id=bot_id)
    return render(request, 'bot_detail.html', {'bot': bot})

def generate_post(request, bot_id):
    """
    View function to generate a post for a specific bot.
    """
    if request.method == 'POST':
        bot = Bot.objects.get(id=bot_id)
        subject = request.POST.get('subject')
        post = bot.generate_post(subject)
        return redirect('bot_detail', bot_id=bot_id)
    else:
        return render(request, 'generate_post.html')

