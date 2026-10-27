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

def draw_add_screen(screen):
    # Khai báo lấy biến toàn cục ở bên ngoài vào hàm
    global input_front, input_back, active_box, status_message, vocab_list

    screen.fill(WHITE)
    #Vẽ tựa đề màn hình, vị trí chính giữa, cách lề 60px
    title_surf = FONT_TITLE.render("THÊM TỪ VỰNG MỚI", True, BLUE)
    screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 60))

    # Nhãn và Ô nhập Mặt Trước (Front)
    lbl_front = FONT_TEXT.render("Từ vựng (Mặt trước):", True, BLACK)
    screen.blit(lbl_front, (200, 140)) #tạo một label
    box_front = pygame.Rect(200, 170, 400, 45) #Đóng vai trò như một button
    #users click box_front-> active_box = 1 thì đổi viền xanh để người dùng biết đã bấm trúng
    color_f = BLUE if active_box == 1 else GRAY
    pygame.draw.rect(screen, LIGHT_GRAY, box_front, border_radius=8) #vẽ nền ô và viền ô tròn góc
    pygame.draw.rect(screen, color_f, box_front, 2, border_radius=8)
    txt_f = FONT_TEXT.render(input_front, True, BLACK)
    screen.blit(txt_f, (box_front.x + 10, box_front.y + 10)) #hiển thị chuỗi ký tự input_front (users nhập) vào ô

    # Nhãn và Ô nhập Mặt Sau (Back)
    lbl_back = FONT_TEXT.render("Ý nghĩa (Mặt sau):", True, BLACK)
    screen.blit(lbl_back, (200, 230))
    box_back = pygame.Rect(200, 260, 400, 45)
    color_b = BLUE if active_box == 2 else GRAY
    pygame.draw.rect(screen, LIGHT_GRAY, box_back, border_radius=8)
    pygame.draw.rect(screen, color_b, box_back, 2, border_radius=8)
    txt_b = FONT_TEXT.render(input_back, True, BLACK)
    screen.blit(txt_b, (box_back.x + 10, box_back.y + 10))

    # Thông báo trạng thái (vd: "Đã thêm từ thành công!")
    if status_message:
        msg_surf = FONT_TEXT.render(status_message, True, GREEN)
        screen.blit(msg_surf, (SCREEN_WIDTH // 2 - msg_surf.get_width() // 2, 320))

    # Nút Lưu Từ
    btn_save = pygame.Rect(200, 360, 190, 45)
    pygame.draw.rect(screen, GREEN, btn_save, border_radius=8)
    txt_save = FONT_TEXT.render("Lưu Từ Này", True, WHITE)
    screen.blit(txt_save, (btn_save.x + (190 - txt_save.get_width()) // 2, btn_save.y + 12))

    # Nút Bắt Đầu Học Ngay
    btn_goto_study = pygame.Rect(410, 360, 190, 45)
    study_col = BLUE if len(vocab_list) > 0 else GRAY #đếm từ nếu chưa có từ nào thì hiện xám
    pygame.draw.rect(screen, study_col, btn_goto_study, border_radius=8)
    txt_goto = FONT_TEXT.render(f"Học Ngay ({len(vocab_list)})", True, WHITE)
    screen.blit(txt_goto, (btn_goto_study.x + (190 - txt_goto.get_width()) // 2, btn_goto_study.y + 12))

    # Nút Quay lại Menu
    btn_back = pygame.Rect(200, 420, 400, 40)
    pygame.draw.rect(screen, GRAY, btn_back, border_radius=8)
    txt_back = FONT_TEXT.render("Quay lại Menu", True, BLACK)
    screen.blit(txt_back, (btn_back.x + (400 - txt_back.get_width()) // 2, btn_back.y + 10))
    '''
    - Kiểm tra giá trị active box -> Hiện màu khi =1, =2 và none (cách đổi giá trị ở phần main loop) 
    -> Active_box =1/2 thì ghi biến vào input_front/input_back
    - Hiện thị chữ đang gõ bằng lệnh render và in chuỗi input_font (ô nhập 1) và input_back (ô nhập 2)
    -> Hàm ở main loop đóng vai trò là đếm ký tự để xác định users đã nhập -> Đọc biến và in chữ lên ô
    Khi input_front và input_back có chuỗi -> Hiện status_message -> Lưu vào danh sách vocab_list 
    -> Xóa biến ở 2 ô nhớ đó để tiếp tục nhận chuỗi tiếp theo
    '''
    return box_front, box_back, btn_save, btn_goto_study, btn_back

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