import pygame
import random 

pygame.init()
screen = pygame.display.set_mode((800, 600))

font_t = pygame.font.SysFont(None, 30)
restart_btn_rect = pygame.Rect(300, 480, 200, 50)


def draw_text(text, font =font_t, text_color = (0,0,0), x=300,y=100):
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y))

def draw_button():
    pygame.draw.rect(screen, ( 255,51,51), restart_btn_rect)
    text = font_t.render("Restart Game", True, (255, 255, 204))
    screen.blit(text, (restart_btn_rect.x + 30, restart_btn_rect.y + 10))

attempts = 10
        
def reset_game():
    global word, word_not_guessed, letters, attempts, letter, message, message2
    word = random.choice(word_bank)
    word_not_guessed = " _" * len(word)
    letters = []
    attempts = 10
    letter = ""
    message = font_t.render("", True, (0, 0, 0))
    message2 = font_t.render("", True, (0, 0, 0))


pygame.display.set_caption("Word Guesser")
icon = pygame.image.load("avocado.png")
pygame.display.set_icon(icon)
letters = []
letter = ""
word_bank = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew']
word = random.choice(word_bank)
word_not_guessed = len(word) * " _"
running = True
message = font_t.render("", True, (0, 0, 0))
message2 = font_t.render("", True, (0, 0, 0))
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_btn_rect.collidepoint(event.pos):
                reset_game()
        
        if attempts > 0 and event.type == pygame.KEYDOWN:
            letter = event.unicode
            if letter.isalpha() and len(letter) == 1:
               letters.append(letter.lower())
            else:
                message = font_t.render("Please enter a single letter.", True, (255,0,0))
                
            if letter in word:
                word_not_guessed = "".join([c if c in letters else " _" for c in word])
                message = font_t.render("Good guess!", True, (0, 255, 0))
            else:
                attempts -= 1
                message = font_t.render("Sorry, that letter is not in the word.", True, (255, 0, 0))

            message2 = font_t.render(f"You guessed: {word_not_guessed}", True, (0, 255, 0))

    screen.fill((204, 255,229))
 
    draw_text(f"Word: {word_not_guessed}", y=150)
    draw_text(f"Attempts left: {attempts}", y=200)
    draw_text(f"Last guess: {letter}", y=250)
    screen.blit(message, (350, 300))
    screen.blit(message2, (350, 350))

    if "_" not in word_not_guessed:
        win_msg = font_t.render(f"Congratulations! You guessed the word: {word}", True, (0, 128, 0))
        screen.blit(win_msg, (150, 400))
        draw_button()
    elif attempts == 0:
        lose_msg = font_t.render(f"Sorry, you lost. The word was: {word}", True, (255, 0, 0))
        screen.blit(lose_msg, (150, 400))
        draw_button()

    pygame.display.flip()

pygame.quit()