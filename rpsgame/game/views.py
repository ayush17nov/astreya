import requests
import logging
import datetime

from random import choices
from django.shortcuts import redirect, render


logger = logging.getLogger(__name__)

selection_list = ["rock", "paper", "scissors"]
rules = {
	("rock", "paper"): "won",
	("rock", "scissors"): "lost",
	("paper", "scissors"): "won",
	("paper", "rock"): "lost",
	("scissors", "rock"): "won",
	("scissors", "paper"): "lost",
}
user_playing = None
round = user_wins = user_ties = user_loose = player_score = 0

def reset():
    global user_playing, round, user_wins, user_ties, user_loose, player_score
    round = user_wins = user_ties = user_loose = player_score = 0
    user_playing = None

def reset_game():
    global round, user_wins, user_ties, user_loose, player_score
    round = user_wins = user_ties = user_loose = player_score = 0

def play_game(user_choice, round, user, player_score):
    comp_choice = choices(selection_list)[0]
    msg = "Round %r - %r has selected %r, Score %r at %r hours!"%(round, user, user_choice, player_score, str(datetime.datetime.now()))
    logger.debug(msg)
    msg = "Round %r - Bot has selected %r at %r hours!"%(round, comp_choice, str(datetime.datetime.now()))
    logger.debug(msg)
    if comp_choice == user_choice:
        return "tie"
    else:
        return rules[comp_choice, user_choice]

def check_game_winning(wins, ties, loose):
    if wins >= 2 or (ties == 1 and wins >= 2) or (ties == 2 and wins >= 1):
        return "won"
    elif ties > 2 or wins == loose:
        return "ties"
    else:
        return "lost"

def index(request):
    reset()
    return render(request, 'index.html', {})

def home(request):
    user = request.POST.get('name')
    if user:
        r = requests.post('http://127.0.0.1:8000/api/', data={'name': user})
        status = r.status_code
        if status == 201 or status == 302:
            global user_playing
            user_playing = user
            reset_game()
            return render(request, 'home.html', {'user': user_playing})
    return redirect("/")

def start_game(request, user_choice=None):
    global user_playing
    if user_choice == "newgame":
        reset_game()
        return render(request, 'home.html', {'user': user_playing})
    else:
        global round, user_wins, user_ties, user_loose, player_score
        if round < 3:
            round = round+1
        else:
            round = 1
        result = play_game(user_choice, round, user_playing, player_score)
        if result == "won":
            user_wins += 1
            player_score += 1
        elif result == "ties":
            user_ties += 1
        else:
            user_loose += 1
        final_result = None
        if round == 3:
            final_result = check_game_winning(user_wins, user_ties, user_loose)
            result = None
        return render(request, "home.html", {"result": result, "round": round, 'user': user_playing, "final_result": final_result})
