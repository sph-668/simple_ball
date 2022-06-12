from tkinter import *
import random
import time
import pickle


class Ball:
    def __init__ (self, canvas, paddle, color):
        
        self.canvas = canvas
        self.paddle = paddle
        
        self.marks = 0
        #объявление переменной текущего счёта

        self.myscore = self.canvas.create_text(80, 18, text = 'Мой счёт:' + str(self.marks), fill = 'red', font = ('Times', 22))
        
        self.id = canvas.create_oval(10, 10, 30, 30, fill=color)
        #создание макета мячика
        self.canvas.move(self.id, 245, 100)
        #перемещение мячика в точку с координатами (245,100)


        
        
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        #случайный выбор направления полета мячика

        
        self.canvas_height = self.canvas.winfo_height()
        #текущая высота холста
        self.canvas_width = self.canvas.winfo_width()
        #текущая ширина холста

        self.hit_bottom = False







    def hit_paddle(self, pos):
    #передаём текущие координаты мяча
        paddle_pos = self.canvas.coords(self.paddle.id)
        #получаем текущие координаты ракетки
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
                #произошло столкновение с ракеткой
            return False
    


    def record(self, previous_marks):
    #проверяем, установлен ли новый рекорд
        if self.marks > previous_marks:
            #сравнение прошлого рекорда с настоящим счётом
            save_file = open('tools/save.dat', 'wb')
            pickle.dump(self.marks, save_file)
            #запись нового рекорда в файл
            save_file.close()
            return True
    


        
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        #функция перемещения мячика на величины x и y
        pos = self.canvas.coords(self.id)
        #массив с текущими координатами мячика


        if pos[3] >= self.canvas_height:
            #проверка мячика на столкновение с нижней границей (окончание игры)
            self.hit_bottom = True      
            self.record(previous_marks)
            #проверка на рекорд



        if self.hit_paddle(pos) == True:
            #проверка на столкновение мячика с ракеткой
            self.marks += 1
            #начисление очков за отбитый мячик
            canvas.itemconfig(self.myscore, text = 'Мой счёт: ' + str(self.marks))
            #обновление счёта
            self.y = -3
        
        
        
      
        if pos[1] <= 30:
            #проверка мячика на столкновение с верхней границей поля
            self.y = 3        

            
            
        if pos[0] <= 0:
            #проверка мячика на столкновение с левой границей
            self.x = 3


            
            
        if pos[2] >= self.canvas_width:
            #проверка мячика на столкновение с правой границей поля
            self.x = -3




class Paddle:
    def __init__ (self, canvas, color):
        
        self.canvas = canvas
        self.begin_l = False
        self.begin_r = False
        self.id = canvas.create_rectangle(0, 0, 130, 12, fill=color)
        #создание макета ракетки
        self.canvas.move(self.id, 200, 400)
        #перемещение ракетки в точку с координатами (200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        #привязка на нажатие клавиши влево
        self.canvas.bind_all('<KeyPress-Right>', self.move_right)
        #привязка на нажатие клавиши вправо


    def move_left(self, evt):
        self.x = -3
        #смещение влево при нажатии влево
        
    def move_right(self, evt):
        self.x = 3
        #смещение вправо при нажатии вправо


    


    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0
        #проверка ракетки на столкновение с краями поля


        






tk = Tk()
tk.title("Шарик")
#заголовок игры
tk.resizable(0, 0)

tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=450, bd=0, highlightthickness=0)
#создание холста с параметрами
canvas.pack()
#отображение холста
canvas.create_line(0, 30, 500, 30, fill = 'purple')
#верхняя граница поля
tk.update()
#принудительное обновление 





paddle = Paddle(canvas, 'green')
#создание ракетки
ball = Ball (canvas, paddle, 'red')
#создание мячика




def start (event):
    canvas.itemconfig(please, text = '')
    #убираем с экрана просьбу нажать клавишу "Enter"
    while 1:
        #главный цикл
        if ball.hit_bottom == False:
            ball.draw()
            paddle.draw()
        elif ball.record(previous_marks) == True:
            #проверка на появление нового рекорда
            canvas.create_text(250, 200, text = 'ОГО! Новый рекорд!', fill = 'red', font = ('Times', 40))
            #создание сообщения о новом рекорде
        else:
            canvas.create_text (250, 200, text = '''Ха-ха! Проиграл!''', fill = 'red', font = ('Times', 40)) 
            #сообщение о проигрыше

        tk.update_idletasks()
        tk.update()
        #принудительное обновление экрана
        time.sleep(0.01)
        #задержка на 0.01 секунды

        


load_file = open('tools/save.dat', 'rb')
#открываем загрузочный файл с записанным рекордом
previous_marks = pickle.load(load_file)
#сохраняем предыдущий рекорд в переменную previous_record
load_file.close()
#закрытие загрузочного файла



myrecord = canvas.create_text(400, 20, text = 'Мой рекорд: ' + str(previous_marks), font = ('Times', 20))
#создание поля для записи рекорда




please = canvas.create_text (250, 200, text = '''Нажми "Enter"''', fill = 'orange', font = ('Times', 30))
#начало игры (просьба нажать клавишу)

canvas.bind_all('<KeyPress-Return>', start)
#начало игры при нажатии на Enter









    
