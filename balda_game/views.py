import json
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from balda_game.CellState import SPARE, FIXED
from balda_game.GameManagerProcessor import GameProcessor
from balda_game.Letter import Coordinates
from balda_game.Packer import pack_game_message_with_action, deserialize_int, deserialize_list
from balda_game.SingletonDictionary import dictionary
from balda_game.lang.RussianLanguage import RussianLanguage
from balda_game.models import UserPlayer


def index(request):
    field = [['-' for i in range(5)] for j in range(5)]
    field[2] = ['Б', 'А', 'Л', 'Д', 'А']
    first_word = dictionary.get_first_word(5)
    print(first_word)
    return render(request, 'index.html')


def run_game(request):
    field = [['-' for i in range(5)] for j in range(5)]
    field[2] = ['Б', 'А', 'Л', 'Д', 'А']
    return render(request, 'field.html', {'field': field})


def start_game(request, game_id):
    field = [[['.', SPARE] for i in range(5)] for j in range(5)]
    #TODO check for errors
    word = GameProcessor.list_first_words.get(int(game_id))
    GameProcessor.start_game(int(game_id))
    field[2] = [[letter, FIXED] for letter in word]
    lang_list = RussianLanguage().get_list()
    return render(request, 'field.html', {'field': field, 'game_id': game_id, 'lang_list': lang_list})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user1 = UserPlayer()
            user1.wins = 0
            user1.loses = 0
            user1.draws = 0
            user1.rating = 0
            user1.user = new_user
            user1.save()
            user = UserPlayer.objects.create
            return HttpResponseRedirect('/')
    form = UserCreationForm()
    return render(request, "register.html", {
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', {"message": "Wrong login or password"})
    else:
        return render(request, 'login.html', {})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    user_profile = UserPlayer.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required
def game_wait(request):
    GameProcessor.add_player(request.user)
    return render(request, 'game_wait.html', {})

@login_required
def wait_query(request):
    value = GameProcessor.add_waiting_player(request.user)
    json_result = {'game': value}
    return HttpResponse(json.dumps(json_result), content_type="application/json")

@login_required
def get_field(request, game_id):
    json_result = pack_game_message_with_action(game_id, request.user)
    return HttpResponse(json.dumps(json_result), content_type="application/json")

@login_required
def commit_word(request, game_id):
    game_id = deserialize_int(game_id)
    pinned_height = deserialize_int(request.POST.get('pinned_height', False))
    pinned_width = deserialize_int(request.POST.get('pinned_width', False))
    word = request.POST.get('word', False)
    heights = deserialize_list(request.POST.getlist('heights[]', []))
    widths = deserialize_list(request.POST.getlist('widths[]', []))
    pinned_letter = request.POST.get('pinned_letter', False)
    flag = True
    flag &= GameProcessor.check_board_consistency(game_id, pinned_height, pinned_width, word, heights, widths)
    flag &= dictionary.check_word(game_id, heights, widths, Coordinates(pinned_height, pinned_width), word)
    flag &= GameProcessor.change_move(request.user, game_id, word, pinned_height, pinned_width, pinned_letter)
    if not flag:
        return HttpResponse(pack_game_message_with_action(game_id, request.user, 'reset'),
                            content_type="application/json")
    else:
        return HttpResponse(pack_game_message_with_action(game_id, request.user, 'ok'), content_type="application/json")
