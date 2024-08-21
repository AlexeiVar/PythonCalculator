from tkinter import *
from tkinter.font import Font
from decimal import Decimal  # Для более точных вычислений
from math import sqrt, sin, cos, asin, acos  # Для квадратного корня(заменимо), арккосинуса, арксинуса и тангенса

ops = {"+": lambda x, y: x + y,  # Для реализации равно
       "-": lambda x, y: x - y,
       "*": lambda x, y: x * y,
       '/': lambda x, y: x / y,
       '//': lambda x, y: x // y,
       '**': lambda x, y: x ** y}

CurrentMode = 0
caller = ''  # Для истории
first = None
second = None
method = None  # Все три переменных для реализации доп дисплея и для более простой реализации вычислений
calculated = False  # Служит как флаг для проверки находится ли прямо сейчас результат в дисплее

root = Tk()
root.configure(bg='grey')
DisFont = Font(family='Helvetica', size=30)  # Шрифт для дисплея
ButFont = Font(family='Helvetica', size=28)  # Шрифт для кнопок
ButFontSmall = Font(family='Helvetica', size=20)
# Тоже для кнопок, но поменьше, так как некоторые символы не влезают иначе
HistoryFont = Font(family='Helvetica', size=15)  # Шрифт для истории
root.title('Калькулятор')
root.geometry('320x400')
root.resizable(False, False)  # Для реализации расширенного мода


def Expand():  # Переключение режима
    global CurrentMode
    if CurrentMode == 1:
        mode.configure(text='Стандартный режим')
        root.geometry('320x400')
        CurrentMode = 0
    else:
        mode.configure(text='Расширенный режим')
        root.geometry('505x505')
        CurrentMode = 1


# Дисплей и режим
mode = Label(root, text='Стандартный режим', bg='grey', fg='white')  # Текст с текущим режимом
mode.place(x=0, y=0)
ExpandBut = Button(root, text="Поменять режим", command=Expand, bg='grey', fg='white')  # Кнопка для смены режима
ExpandBut.place(x=214, y=0)
display = Entry(root, justify=RIGHT, font=DisFont, width=14, bg='grey', fg='white')  # Главный дисплей калькулятора
display.place(x=4, y=56)
SubDisplay = Entry(root, justify=RIGHT, width=15, disabledbackground='grey', disabledforeground='white',
                   state='disabled')  # Доп дисплей калькулятора
SubDisplay.place(x=225, y=35)


def IntoDisplay(x):  # Для записи в дисплей
    global calculated
    y = display.get()
    if x == '.' and y.find('.') != -1:
        return
    if calculated is False:  # Позволит стереть ответ при наборе нового числа
        x = str(x)
        display.insert(END, x)
    else:
        display.delete(0, END)
        x = str(x)
        display.insert(END, x)
        calculated = False


def Negative():  # Функция или делает число отрицательным или положительным
    y = display.get()
    if y.find('-') == -1:
        display.delete(0, END)
        display.insert(0, '-' + y)
    else:
        display.delete(0, END)
        display.insert(0, y.replace('-', ''))


def MoveToSub(x):  # Перемешение в доп дисплей
    global method, first
    working = True
    while working:  # Позволяет проводить несколько операций не нажимая =
        if SubDisplay.get() == "":
            y = display.get()
            method = x
            if y.find('.') == -1:
                first = int(display.get())
            else:
                first = Decimal(display.get())
            SubDisplay.configure(state='normal')
            SubDisplay.insert(END, display.get() + x)
            SubDisplay.configure(state='disabled')
            display.delete(0, END)
            working = False
        else:
            Calculate()


def Calculate():  # Вычисление и запись ответа
    global method, first, second, calculated
    y = display.get()
    if y.find('.') == -1:
        second = int(display.get())
    else:
        second = Decimal(display.get())
    if (method == "/" or method == '//') and second == 0:  # Для предотвращения деления на 0
        Clear()
        display.insert(0, "Ошибка")
        calculated = True
        first = None
        second = None
        method = None
        return
    if method in ops:  # Проверяю метод в операциях и делаю вычисление
        display.delete(0, END)
        SubDisplay.configure(state='normal')
        SubDisplay.delete(0, END)
        SubDisplay.configure(state='disabled')
        display.insert(0, ops[method](first, second))
        record('normal', 0)
        calculated = True
        first = None
        second = None
        method = None
    else:  # В случии если просто ввести число и нажать =, то ничего не случится
        pass


def Clear():  # Очистка всего, используется так как в лямбду не вместилась бы комманда
    global first, method
    display.delete(0, END)
    SubDisplay.configure(state='normal')
    SubDisplay.delete(0, END)
    SubDisplay.configure(state='disabled')
    first = None
    method = None


def SquareRoot():  # Функция для вычисления корня, не использует = так как требует только одно число
    global calculated, caller
    y = display.get()
    display.delete(0, END)
    if y == '':
        y = '0'
    if y.find('.') == -1:
        y = int(y)
    else:
        y = Decimal(y)
    if y < 0:
        display.insert(0, "Ошибка")
    else:
        display.insert(0, sqrt(y))
        caller = '√'
        record('not', y)
        caller = ''
    calculated = True


class MainFrame:  # Весь функционал обычного режима кроме памяти, дисплеев и смены режима

    def __init__(self, master):
        my_frame = Frame(master, bg='grey')
        my_frame.place(x=0, y=105, width=330, height=295)
        r = 0
        for i in range(1, 10):  # Создание кнопок от 1 до 9
            r += 0.33  # Для правильного вычисленния ряда
            Button(my_frame, text=i, font=ButFont, command=lambda i=i: IntoDisplay(i)).grid(row=2 - int(r),
                                                                                            column=(i - 1) % 3)
        # Так как 0 . и ± не влезут в формулу я их ставлю отдельно
        Button(my_frame, text='0', font=ButFont, command=lambda: IntoDisplay(0)).grid(row=3, column=1)
        Button(my_frame, text='.', font=ButFont, command=lambda: IntoDisplay('.'), height=1, width=2) \
            .grid(row=3, column=2)
        Button(my_frame, text='±', font=ButFont, height=1, width=2, command=Negative).grid(row=3, column=0)

        butrange = ('+', "*", '-', '/', '**')  # Для базовых операций
        r = 0
        c = 4
        for operation in butrange:
            Button(my_frame, text=operation, font=ButFont, height=1, width=2, bg='grey', fg='white',
                   command=lambda operation=operation: MoveToSub(operation)).grid(row=int(r), column=c)
            # Создаю кнопку с операцией
            r += 0.5
            if c == 4:  # Меняю колонну в которую идет кнопка
                c = 5
            else:
                c = 4
        Button(my_frame, text='√', font=ButFont, height=1, width=2, bg='grey', fg='white', command=SquareRoot) \
            .grid(row=2, column=5)  # Так как используется другая комманда, создаю квадратный корень отдельно

        Button(my_frame, text='⌫', font=ButFont, command=lambda: display.delete(len(display.get()) - 1, END), bg='Red',
               fg='white', height=1, width=2).grid(row=0, column=6)
        Button(my_frame, text='CE', font=ButFont, command=lambda: display.delete(0, END), height=1, width=2,
               bg='Red', fg='white').grid(row=1, column=6)
        Button(my_frame, text='C', font=ButFont, command=Clear, bg='Red', fg='white', height=1, width=2) \
            .grid(row=2, column=6)
        Button(my_frame, text='=', font=ButFont, command=lambda: Calculate(), height=1, width=4, bg='LightBlue') \
            .grid(row=3, column=4, columnspan=2)


class MemoryCell:  # Класс для одной ячейки памяти, он принимает сам root, свой индекс (номер ячейки) и свою позицию
    # Выбрал создавать по одной ячейки для более легкой работы с ними,
    # это повзоляет например поставить ячейку в базовый режим

    def __init__(self, master, index, posx, posy):
        my_frame = Frame(master)  # Фрейм для хранения всей ячейки
        my_frame.place(x=posx, y=posy)
        self.index = index
        self.number = 0  # Само число
        self.MC = Button(my_frame, text="MC%s" % self.index, command=self.clear, state='disabled', bg='grey',
                         fg='white')
        self.MC.grid(row=0, column=0)
        self.MR = Button(my_frame, text="MR%s" % self.index, command=self.input, state='disabled', bg='grey',
                         fg='white')
        self.MR.grid(row=0, column=1)
        self.MPlus = Button(my_frame, text="M%s+" % self.index, command=self.plus, bg='grey', fg='white')
        self.MPlus.grid(row=0, column=2)
        self.MMinus = Button(my_frame, text="M%s-" % self.index, command=self.minus, bg='grey', fg='white')
        self.MMinus.grid(row=0, column=3)
        self.MSave = Button(my_frame, text="MS%s" % self.index, command=self.save, bg='grey', fg='white')
        self.MSave.grid(row=0, column=4)

    def clear(self):  # Функция для очистки ячейки
        self.number = 0
        self.MC.configure(state='disabled')
        self.MR.configure(state='disabled')

    def input(self):  # Функция для записи из ячейки в дисплей
        global calculated
        display.delete(0, END)
        display.insert(0, self.number)
        calculated = True

    def plus(self):  # Функция для добавления числа из дисплея к числу из ячейки
        y = display.get()
        if y == "":
            y = 0
        else:
            if y.find('.') == -1:
                y = int(display.get())
            else:
                y = Decimal(display.get())
        self.number += y
        self.MC.configure(state='normal')
        self.MR.configure(state='normal')

    def minus(self):  # Функция для вычитания из числа ячейки числа на дисплее
        y = display.get()
        if y == "":
            y = 0
        else:
            if y.find('.') == -1:
                y = int(display.get())
            else:
                y = Decimal(display.get())
        self.number -= y
        self.MC.configure(state='normal')
        self.MR.configure(state='normal')

    def save(self):  # Функция для записи числа из дисплея в ячейку
        y = display.get()
        if y == "":
            y = 0
        self.number = int(y)
        self.MC.configure(state='normal')
        self.MR.configure(state='normal')


def arc(x):  # Для вычисления арк синуса и косинуса
    global calculated, caller
    y = display.get()
    if y.find('.') == -1:
        y = int(y)
    else:
        y = Decimal(y)
    display.delete(0, END)
    if y > 1 or y < -1:
        display.insert(0, "Ошибка")
        calculated = True
        return
    if x == "cos":
        display.insert(0, "%.10f" % acos(y))
        caller = 'acos'
        record('not', y)
        caller = ''
    else:
        display.insert(0, "%.10f" % asin(y))
        caller = 'asin'
        record('asin', y)
        caller = ''
    calculated = True


def TenToPower():  # Так как не могу в лямбду больше одной строки записать, использую функцию
    Clear()
    display.insert(0, '10')
    MoveToSub('**')


def Cotangent():  # вычисление котангенса
    global calculated, caller
    y = display.get()
    if y.find('.') == -1:
        y = int(y)
    else:
        y = Decimal(y)
    display.delete(0, END)
    display.insert(0, "%.10f" % (cos(y) / sin(y)))
    caller = 'ctg'
    record('not', y)
    caller = ''
    calculated = True


class ExtraFunctions:  # Класс под экстра функции

    def __init__(self, master):
        my_frame = Frame(master, bg='grey')
        my_frame.place(x=0, y=401, width=250, height=120)  # Фрейм для кнопок

        Button(my_frame, text='acos', font=ButFontSmall, command=lambda: arc(cos), bg='grey', fg='white',
               height=1, width=4).grid(row=0, column=0, columnspan=2)
        Button(my_frame, text='asin', font=ButFontSmall, command=lambda: arc(sin), bg='grey', fg='white',
               height=1, width=4).grid(row=1, column=0, columnspan=2)
        Button(my_frame, text='ctg', font=ButFontSmall, command=Cotangent, bg='grey', fg='white',
               height=1, width=4).grid(row=0, column=2, columnspan=2)
        Button(my_frame, text='//', font=ButFontSmall, command=lambda: MoveToSub('//'), bg='grey', fg='white',
               height=1, width=2).grid(row=0, column=4)
        Button(my_frame, text='10^x', font=ButFontSmall, command=TenToPower, bg='grey', fg='white', height=1, width=4) \
            .grid(row=1, column=2, columnspan=2)


ResultHistory = {0: "", 1: "", 2: "", 3: "", 4: ""}  # Для реализации истории
OperationHistory = {0: "", 1: "", 2: "", 3: "", 4: ""}


def record(x, y):  # Для записи в историю
    global method, first, second, caller
    for i in range(0, 4):
        ResultHistory[(4 - i)] = ResultHistory[(3 - i)]
        OperationHistory[(4 - i)] = OperationHistory[(3 - i)]
    if x == 'normal':  # Для стандартных операторов
        OperationHistory[0] = ('%s%s%s' % (first, method, second))
    else:  # Для операторов которые требуют только одно число
        OperationHistory[0] = ('%s(%s)' % (caller, y))
    ResultHistory[0] = ('=%s' % display.get())
    RowOne.update()  # В случаи расширения истории, нужно добавить еще одну строку суда
    RowTwo.update()
    RowThree.update()
    RowFour.update()
    RowFive.update()


class HistorySet:  # Реализация пары истории уравнение+решение

    def __init__(self, master, index):
        my_frame = Frame(master, bg='grey')
        my_frame.grid(row=index, column=0)
        self.index = index
        self.operation = Label(my_frame, text=OperationHistory[self.index], font=HistoryFont, bg='grey', fg='white')
        self.operation.grid(row=0, column=0)
        self.result = Label(my_frame, text=ResultHistory[self.index], font=HistoryFont, bg='grey', fg='white')
        self.result.grid(row=1, column=0)

    def update(self):
        self.operation.configure(text=OperationHistory[self.index])
        self.result.configure(text=ResultHistory[self.index])


# Создаю фрейм для всех пар истории
HistoryFrame = Frame(root, highlightbackground="black", highlightthickness=2, bg='grey')
HistoryFrame.place(x=330, y=205, width=172, height=310)

# Сам калькулятор
RowOne = HistorySet(HistoryFrame, 0)
RowTwo = HistorySet(HistoryFrame, 1)
RowThree = HistorySet(HistoryFrame, 2)
RowFour = HistorySet(HistoryFrame, 3)
RowFive = HistorySet(HistoryFrame, 4)
keyboard = MainFrame(root)
extra = ExtraFunctions(root)
MemoryCell(root, 1, 0, 25)  # Ячейка, которая идет в обычный режим
# С текущим расположением, индекс ячейки может быть только одним символом
y = 0
for i in range(2, 10):
    MemoryCell(root, i, 330, y)
    y += 25

root.mainloop()
