import os
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Guesser")

# load the icon relative to this file so the game works from any folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon = pygame.image.load(os.path.join(BASE_DIR, "avocado.png"))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

BG = (234, 246, 235)
PANEL = (255, 255, 255)
PANEL_EDGE = (205, 226, 209)
DARK = (46, 71, 59)
GREEN = (56, 142, 60)
RED = (204, 70, 70)
GREY = (139, 152, 143)
HEART_ON = (226, 80, 80)
HEART_OFF = (223, 229, 224)
BTN = (226, 80, 80)
BTN_HOVER = (240, 104, 104)
BTN_TEXT = (255, 246, 240)

font_title = pygame.font.SysFont("verdana", 34, bold=True)
font_word = pygame.font.SysFont("consolas", 46, bold=True)
font_word_small = pygame.font.SysFont("consolas", 30, bold=True)
font_t = pygame.font.SysFont("verdana", 20)
font_small = pygame.font.SysFont("verdana", 15)

restart_btn_rect = pygame.Rect(WIDTH // 2 - 110, 505, 220, 48)

fruits = ["Apple", "Banana", "Orange", "Mango", "Grape", "Pineapple", "Strawberry",
    "Blueberry", "Watermelon", "Pear", "Peach", "Plum", "Cherry", "Kiwi",
    "Pomegranate", "Guava", "Papaya", "Lemon", "Lime", "Coconut", "Fig",
    "Apricot", "Raspberry", "Cranberry", "Dragonfruit", "Lychee", "Passionfruit",
    "Starfruit", "Tangerine", "Nectarine", "Date", "Blackberry", "Mulberry",
    "Jackfruit", "Durian", "Rambutan", "Soursop", "Cantaloupe", "Honeydew",
    "Persimmon", "Quince", "Ugli fruit", "Gooseberry", "Boysenberry", "Jujube"
]

vegetables = [
    "Carrot", "Broccoli", "Spinach", "Potato", "Tomato", "Cucumber", "Onion",
    "Garlic", "Pepper", "Cabbage", "Cauliflower", "Zucchini", "Lettuce",
    "Eggplant", "Pumpkin", "Radish", "Celery", "Beetroot", "Turnip", "Peas",
    "Green Beans", "Sweet Potato", "Corn", "Leek", "Asparagus", "Artichoke",
    "Brussels Sprouts", "Chard", "Okra", "Kale", "Fennel", "Parsnip", "Scallion",
    "Yam", "Rutabaga", "Mustard Greens", "Bok Choy", "Endive", "Arugula",
    "Watercress", "Daikon", "Horseradish", "Taro", "Collard Greens"]

MAX_ATTEMPTS = 10


def pick_word():
    if random.random() < 0.5:
        return "Fruits", random.choice(fruits).lower()
    return "Vegetables", random.choice(vegetables).lower()


def reset_game():
    global category, word, letters, wrong_letters, attempts, message, message_color, game_over
    category, word = pick_word()
    letters = []
    wrong_letters = []
    attempts = MAX_ATTEMPTS
    message = "Guess the word, one letter at a time."
    message_color = DARK
    game_over = False


def masked_word():
    # spaces in words like "green beans" are revealed automatically
    return " ".join(c.upper() if (c in letters or not c.isalpha()) else "_" for c in word)


def word_is_guessed():
    return all(c in letters or not c.isalpha() for c in word)


def draw_text(text, font=font_t, color=DARK, y=100):
    img = font.render(text, True, color)
    screen.blit(img, img.get_rect(center=(WIDTH // 2, y)))


def draw_word(panel):
    img = font_word.render(masked_word(), True, DARK)
    if img.get_width() > panel.width - 40:
        img = font_word_small.render(masked_word(), True, DARK)
    screen.blit(img, img.get_rect(center=(WIDTH // 2, 210)))


def draw_attempts():
    spacing = 30
    start_x = WIDTH // 2 - spacing * (MAX_ATTEMPTS - 1) // 2
    for i in range(MAX_ATTEMPTS):
        color = HEART_ON if i < attempts else HEART_OFF
        pygame.draw.circle(screen, color, (start_x + i * spacing, 318), 10)


def draw_button():
    hovered = restart_btn_rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, BTN_HOVER if hovered else BTN, restart_btn_rect, border_radius=12)
    text = font_t.render("Restart Game", True, BTN_TEXT)
    screen.blit(text, text.get_rect(center=restart_btn_rect.center))


reset_game()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_btn_rect.collidepoint(event.pos):
                reset_game()

        if event.type == pygame.KEYDOWN and not game_over:
            letter = event.unicode.lower()
            if len(letter) == 1 and letter.isalpha():
                if letter in letters or letter in wrong_letters:
                    message = f"You already tried '{letter.upper()}'."
                    message_color = GREY
                elif letter in word:
                    letters.append(letter)
                    if word_is_guessed():
                        message = f"You won! The word was {word.upper()}."
                        message_color = GREEN
                        game_over = True
                    else:
                        message = "Good guess!"
                        message_color = GREEN
                else:
                    wrong_letters.append(letter)
                    attempts -= 1
                    if attempts == 0:
                        message = f"You lost! The word was {word.upper()}."
                        message_color = RED
                        game_over = True
                    else:
                        message = f"Sorry, no '{letter.upper()}' in the word."
                        message_color = RED
            elif event.unicode:
                message = "Please press a letter key."
                message_color = GREY

    screen.fill(BG)
    draw_text("Word Guesser", font_title, DARK, 52)

    panel = pygame.Rect(60, 92, WIDTH - 120, 382)
    pygame.draw.rect(screen, PANEL, panel, border_radius=18)
    pygame.draw.rect(screen, PANEL_EDGE, panel, width=2, border_radius=18)

    draw_text(f"Category: {category}", font_t, GREY, 138)
    draw_word(panel)
    draw_text("Attempts left", font_small, GREY, 283)
    draw_attempts()
    wrong = ", ".join(w.upper() for w in wrong_letters) if wrong_letters else "-"
    draw_text(f"Wrong letters: {wrong}", font_small, GREY, 362)
    draw_text(message, font_t, message_color, 420)

    if game_over:
        draw_button()
    else:
        draw_text("Type a letter on your keyboard", font_small, GREY, 528)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
