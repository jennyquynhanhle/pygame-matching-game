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
MÀN HÌNH (HÀM GIẢ ĐỂ CHẠY THỬ PHẦN CỦA QANH)
Xóa phần này khi code phần của mình
'''
def draw_menu(screen):
    pass
def draw_add_screen(screen):
    pass
def draw_study(screen):
    screen.fill(WHITE) #Tô toàn bộ màn hình = màu trắng
    
    # Tiến độ
    progress_text = FONT_TEXT.render(f"Từ số: {current_index + 1} / {len(vocab_list)}", True, BLACK) #(Từ số [curren + 1 vì số bắt đầu đếm từ 0] / [số từ tổng], bật khử răng cưa, chữ màu đen)
    screen.blit(progress_text, (50, 30)) #in chữ ra màn hình ở toạ độ x=50, y=30
    
    # Khung Thẻ Flashcard
    card_rect = pygame.Rect(200, 120, 400, 250) #pygame.Rect(x, y, width, height)
    if not is_flipped:
        card_color = LIGHT_GRAY 
    else:
        card_color = (230, 240, 255) #Nếu chưa được lật thì màu light gray, nếu được lật r thì màu (R=230,G=240,B=255) -> màu xanh nhạt gần với màu trắng
    pygame.draw.rect(screen, card_color, card_rect, border_radius=15) # (nơi vẽ, màu nền thẻ, vịtrí và kích thước, bo tròn các góc)
    pygame.draw.rect(screen, BLUE, card_rect, 2, border_radius=15) # (nơi vẽ, màu đường viền, độ dày đường viền, bo tròn góc) do có độ dày đường viền -> biết là tô đường viền
    
    # Nội dung thẻ
    current_card = vocab_list[current_index] #nd thẻ = trích 1 từ ở vị trí ... trong vocab_list
    if not is_flipped:
        content = current_card['front'] 
    else:
        content = current_card['back'] # nd hiển thị trên thẻ = mặt trc current card nếu chưa đc lật, mặt sau current card nếu đc lật r
    text_surf = FONT_CARD.render(content, True, BLACK) #render biến nd chữ hiển thị lên mh # bề mặt chứa h/ả = phông chữ.render (nd thẻ, bật khử răng cưa, màu đen)
    screen.blit(text_surf, (card_rect.x + (400 - text_surf.get_width()) // 2, card_rect.y + 110))
    # 400 (độ dài của thẻ) - cd chữ = khoảng trống, khoảng trống/2 -> mối mép chữ cách đều 2 mép thẻ bnhieu + mép trái mh (x)
    # y + 110 -> chữ cách mép trên thẻ 110 pixel
    
    tip_surf = FONT_TEXT.render("(Click vào thẻ hoặc bấm SPACE để lật)", True, GRAY)
    screen.blit(tip_surf, (SCREEN_WIDTH // 2 - tip_surf.get_width() // 2, 390))
    
    # Nút đánh giá
    btn_unknown = pygame.Rect(200, 450, 180, 50) 
    btn_known = pygame.Rect(420, 450, 180, 50)
    
    pygame.draw.rect(screen, RED, btn_unknown, border_radius=8) #vẽ nền cho các nút
    pygame.draw.rect(screen, GREEN, btn_known, border_radius=8)
    
    txt_unknown = FONT_TEXT.render("Chưa thuộc", True, WHITE)
    txt_known = FONT_TEXT.render("Đã thuộc", True, WHITE)
    
    screen.blit(txt_unknown, (btn_unknown.x + (180 - txt_unknown.get_width()) // 2, btn_unknown.y + 15))
    screen.blit(txt_known, (btn_known.x + (180 - txt_known.get_width()) // 2, btn_known.y + 15))
    
    # Nút quay về Menu giữa chừng
    btn_exit = pygame.Rect(50, 530, 120, 35)
    pygame.draw.rect(screen, GRAY, btn_exit, border_radius=5)
    txt_exit = FONT_TEXT.render("Thoát", True, BLACK)
    screen.blit(txt_exit, (btn_exit.x + (120 - txt_exit.get_width()) // 2, btn_exit.y + 7))
    
    return btn_unknown, btn_known, card_rect, btn_exit
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
