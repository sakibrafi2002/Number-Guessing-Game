from django.shortcuts import render, redirect
from django.views import View
import random

# Constants for game session keys and max attempts
GAME_RANDOM_NUMBER_KEY = 'random_number'
GAME_ATTEMPTS_KEY = 'attempts'
GAME_MAX_ATTEMPTS = 6

class StartGameView(View):
    """
    View to initialize a new game session:
    - Sets a random number between 1 and 100 in session.
    - Resets the number of attempts to 0 in session.
    """
    def get(self, request):
        request.session[GAME_RANDOM_NUMBER_KEY] = random.randint(1, 100)
        request.session[GAME_ATTEMPTS_KEY] = 0
        return render(request, 'guessing_game/start_game.html')


class MakeGuessView(View):
    def post(self, request):
        # Retrieve the user's guess from POST data
        guess_value = request.POST.get('guess')

        # Validate that guess_value is not None and is a valid digit
        if guess_value is None or not guess_value.isdigit():
            result = "Invalid input! Please enter a number between 1 and 100."
            return render(request, 'guessing_game/game_play.html', {
                'result': result,
                'attempts_left': GAME_MAX_ATTEMPTS - request.session.get(GAME_ATTEMPTS_KEY, 0),
                'game_over': False
            })

        # Convert the validated guess to an integer
        user_guess = int(guess_value)

        # Retrieve the game state from session
        random_number = request.session.get(GAME_RANDOM_NUMBER_KEY)
        attempts = request.session.get(GAME_ATTEMPTS_KEY, 0) + 1
        request.session[GAME_ATTEMPTS_KEY] = attempts  # Update the attempts count in session

        # Check if the user's guess is correct
        if user_guess == random_number:
            result = f"Congratulations! You guessed correctly in {attempts} attempts."
            game_over = True
        elif attempts >= GAME_MAX_ATTEMPTS:
            result = f"Sorry, you've used all attempts. The correct number was {random_number}."
            game_over = True
        else:
            # Provide feedback if the guess is incorrect and game is not over
            result = "Too low! Try a higher number." if user_guess < random_number else "Too high! Try a lower number."
            game_over = False

        # Render the gameplay page with the result and game state
        return render(request, 'guessing_game/game_play.html', {
            'result': result,
            'attempts_left': GAME_MAX_ATTEMPTS - attempts,
            'game_over': game_over
        })

    def get(self, request):
        # Redirect to the start game page if accessed via GET
        return redirect('start_game')
