import pygame
import sys

'''
THÔNG SỐ CHUNG
'''
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FLASHCARDS GAME!!!")
clock = pygame.time.Clock()

'''
MÀU SẮC
'''
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
GRAY = (200, 200, 200)
LIGHT_GRAY = (245, 245, 245)
BLUE = (70, 130, 180)
GREEN = (60, 179, 113)
RED = (220, 20, 60)

'''
FONT CHỮ
'''

FONT_TITLE = pygame.font.SysFont("Arial", 36, bold = True)
FONT_TEXT = pygame.font.SysFont("Arial", 20)
FONT_CARD = pygame.font.SysFont("Arial", 28, bold = True)

'''
QUẢN LÝ TRẠNG THÁI GAME
'''

vocab_list = []
current_index = 0
is_flipped = False
score_know = 0
score_unknow = 0

'''
MÀN HÌNH NHẬP TỪ
'''
input_front = ""
input_back = ""
active_box = None 
#Nếu active_box == "front" thì cộng chữ vào input_front và ngược lại.
status_message = "" #Lưu văn bản thông báo sẽ được hiển thị

'''
TRẠNG THÁI GAME 
'''
game_state = "MENU" #MENU --> "ADD" --> "STUDY" --> "RESULT"


'''
MÀN HÌNH MENU CHÍNH
'''
def draw_menu(screen):
    screen.fill(WHITE)

    # Vẽ tiêu đề chính
    title_surf = FONT_TITLE.render("FLASHCARD GAME", True, BLUE)
    screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 150))

    # Nút Thêm Từ Vựng
    btn_add = pygame.Rect(SCREEN_WIDTH // 2 - 150, 260, 300, 50)
    pygame.draw.rect(screen, BLUE, btn_add, border_radius=10)
    txt_add = FONT_TEXT.render("1. Add new vocab", True, WHITE)
    screen.blit(txt_add, (btn_add.x + (300 - txt_add.get_width()) // 2, btn_add.y + 15))

    # Nút Bắt Đầu Học (Chỉ sáng xanh lên nếu đã có ít nhất 1 từ, ngược lại màu xám)
    btn_study = pygame.Rect(SCREEN_WIDTH // 2 - 150, 330, 300, 50)
    study_color = GREEN if len(vocab_list) > 0 else GRAY
    pygame.draw.rect(screen, study_color, btn_study, border_radius=10)
    txt_study = FONT_TEXT.render(f"2. Start learning ({len(vocab_list)} word)", True, WHITE)
    screen.blit(txt_study, (btn_study.x + (300 - txt_study.get_width()) // 2, btn_study.y + 15))

    return btn_add, btn_study

def draw_add_screen(screen):
    pass
def draw_study(screen):
    pass
def draw_result(screen):
    pass

'''
MAIN GAME LOOP
'''

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #nhấn X thì sẽ thoát

        if event.type == pygame.KEYDOWN:
            if game_state == "ADD":
                if active_box == 1:
                    if event.key == pygame.K_BACKSPACE:
                        input_front = input_front[:-1]
                    else:
                        input_front = input_front + event.unicode
                if active_box == 2:
                    if event.key == pygame.K_BACKSPACE:
                        input_back = input_back[:-1]
                    else:
                        input_back = input_back + event.unicode
            # Nhấn phím SPACE để lật thẻ
            if game_state == "STUDY":
                if event.key == pygame.K_SPACE:
                    is_flipped = not is_flipped
        # Xử lý click chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # 1. game_state = "MENU"
            if game_state == "MENU":
                btn_add, btn_study = draw_menu(screen)
                if btn_add.collidepoint(pos):
                    game_state = "ADD"
                    status_message = ""
                if btn_study.collidepoint(pos):
                    if len(vocab_list) > 0:
                        game_state = "STUDY"
                        current_index = 0
                        score_know = 0
                        score_unknow = 0
                        is_flipped = False

            # 2. game_state == "ADD"
            if game_state == "ADD":
                box_front, box_back, btn_save, btn_goto_study, btn_back = draw_add_screen(screen)

                #Khi click vào ô nhập liệu
                if box_front.collidepoint(pos):
                    active_box = 1
                if box_back.collidepoint(pos):
                    active_box = 2
                else:
                    active_box = None

                # Lưu từ
                if btn_save.collidepoint(pos):
                    if input_front.strip() and input_back.strip():
                        vocab_list.append({"front" : input_front.strip(), "back" : input_back.strip()})
                        input_front = "" 
                        input_back = ""
                        status_message = "Đã lưu từ vựng thành công!"
                    else:
                        status_message = "Vui lòng nhập từ vựng và nghĩa!"

                #Click Bắt đầu học
                if btn_goto_study.collidepoint(pos):
                    if len(vocab_list) > 0:
                        current_index = 0
                        score_know = 0
                        score_unknow = 0
                        is_flipped = False

                #Click quay lại MENU
                if box_back.collidepoint(pos):
                    game_state = "MENU"    

            #3. game_state == "STUDY"
            if game_state == "STUDY":
                btn_unknow, btn_know, card_rect, btn_exit = draw_study(screen)

                if card_rect.collidepoint(pos):
                    is_flipped = not is_flipped
                if btn_unknow.collidepoint(pos):
                    score_unknow = score_unknow + 1
                    is_flipped = False
                    current_index = current_index + 1
                    if current_index >= len(vocab_list):
                        game_state = "RESULT"
                if btn_know.collidepoint(pos):
                    score_know = score_know + 1
                    is_flipped = False
                    current_index = current_index + 1
                    if current_index >= len(vocab_list):
                        game_state = "RESULT"
                if btn_exit.collidepoint(pos):
                    game_state = "MENU"

            # 4. game_state == "RESULT"
            if game_state == "RESULT":
                btn_restart = draw_result(screen)
                if btn_restart.collidepoint(pos):
                    game_state = "MENU"

    #Hiển thị giao diên
    if game_state == "MENU":
        draw_menu(screen)
    if game_state == "ADD":
        draw_add_screen(screen)
    if game_state == "STUDY":
        draw_study(screen)
    if game_state == "RESULT":
        draw_result(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()