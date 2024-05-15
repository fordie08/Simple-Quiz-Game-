import pygame
import sys
import time
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('Quiz Game')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Questions and Answers
questions = [
    {"question": "What is the capital of France?", "choices": ["Paris", "London", "Berlin", "Rome"], "answer": "Paris"},
    {"question": "What is 2 + 2?", "choices": ["3", "4", "5", "6"], "answer": "4"},
    {"question": "What is the capital of Italy?", "choices": ["Madrid", "Rome", "Paris", "Berlin"], "answer": "Rome"},
    {"question": "What is 5 * 6?", "choices": ["30", "25", "20", "35"], "answer": "30"},
    {"question": "What is the capital of Spain?", "choices": ["Madrid", "Rome", "Paris", "Berlin"], "answer": "Madrid"},
    {"question": "What is 12 / 4?", "choices": ["2", "3", "4", "5"], "answer": "3"},
    {"question": "What is the capital of Germany?", "choices": ["Paris", "London", "Berlin", "Rome"], "answer": "Berlin"},
    {"question": "What is 9 - 3?", "choices": ["5", "6", "7", "8"], "answer": "6"},
    {"question": "What is the capital of England?", "choices": ["Paris", "London", "Berlin", "Rome"], "answer": "London"},
    {"question": "What is 8 + 2?", "choices": ["9", "10", "11", "12"], "answer": "10"}
]

# Variables
current_question = 0
score = 0
user_name = ''
input_active = False

# Button dimensions
BUTTON_WIDTH = 800
BUTTON_HEIGHT = 50
BUTTON_PADDING = 10

def draw_text(text, font, color, surface, x, y, shadow_color=BLACK):
    shadow = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, color)
    surface.blit(shadow, (x+2, y+2))
    surface.blit(text_surface, (x, y))

def get_user_name():
    global user_name, input_active
    input_box = pygame.Rect(250, 450, 400, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    done = False

    # Load background image for the name input screen
    background = pygame.image.load('images/name_background.png')
    background = pygame.transform.scale(background, (900, 900))

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if input_active:
                    if event.key == K_RETURN:
                        user_name = text
                        done = True
                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    input_active = False
                color = color_active if input_active else color_inactive

        screen.blit(background, (0, 0))

        draw_text('Enter your name:', font, WHITE, screen, 250, 400)
        txt_surface = font.render(text, True, color)
        width = max(400, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

def display_question():
    global current_question
    question_data = questions[current_question]

    # Load background image for the question screen
    background = pygame.image.load(f'images/{current_question + 1}.png')
    background = pygame.transform.scale(background, (900, 900))
    screen.blit(background, (0, 0))

    draw_text(question_data["question"], font, WHITE, screen, 50, 100)

    buttons = []
    for i, choice in enumerate(question_data["choices"]):
        button_rect = pygame.Rect(50, 600 + i * (BUTTON_HEIGHT + BUTTON_PADDING), BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append(button_rect)
        pygame.draw.rect(screen, GRAY, button_rect)
        draw_text(f"{choice}", font, BLACK, screen, 60, 610 + i * (BUTTON_HEIGHT + BUTTON_PADDING))

    pygame.display.flip()
    return buttons

def check_answer(choice):
    global score, current_question
    if questions[current_question]["choices"][choice] == questions[current_question]["answer"]:
        score += 1
        show_feedback("Correct!", 'images/correct.png')
    else:
        show_feedback("Wrong!", 'images/wrong.png')
    current_question += 1
    time.sleep(1)

def show_feedback(text, background_image):
    background = pygame.image.load(background_image)
    background = pygame.transform.scale(background, (900, 900))
    screen.blit(background, (0, 0))
    
    for alpha in range(0, 256, 5):
        feedback_text = large_font.render(text, True, WHITE)
        feedback_text.set_alpha(alpha)
        screen.blit(feedback_text, (300, 400))
        pygame.display.flip()
        pygame.time.delay(10)

def display_score():
    # Load and display the score background image
    background = pygame.image.load('images/score_background.png')
    background = pygame.transform.scale(background, (900, 900))
    screen.blit(background, (0, 0))
    
    # Draw the score text on top of the background with white color
    draw_text(f"{user_name}'s Score: {score} / {len(questions)}", large_font, WHITE, screen, 150, 400)
    
    pygame.display.flip()
    pygame.time.wait(5000)

# Main game loop
def main():
    get_user_name()
    while current_question < len(questions):
        buttons = display_question()
        waiting_for_answer = True

        while waiting_for_answer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for i, button in enumerate(buttons):
                        if button.collidepoint(event.pos):
                            waiting_for_answer = False
                            check_answer(i)

    display_score()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
