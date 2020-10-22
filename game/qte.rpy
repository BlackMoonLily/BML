init python:
    import string

    # переменные (вручную не трогать)
    qte_word = ""
    next_k = ""
    qteTime = .0
    qteMaxTime = 5.0
    abc = list(string.ascii_lowercase)

    # инициализация игры при запуске экрана
    # параметры передаются при вызове экрана игры
    # если слово пустое, то генерируется рандомное длиной length
    # time - время, отведенное на игру в секундах
    def qte_init(word="", time=5.0, length=5):
        global qte_word, next_k, qteMaxTime, qteTime
        qteMaxTime = time
        qteTime = time
        qte_word = word.lower()
        if word:
            next_k = qte_word[0]
        else:
            for i in range(0, length):
                qte_word = qte_word + renpy.random.choice(abc)
                next_k = qte_word[0]
        renpy.restart_interaction()
    # нажатие очередной нужной кнопки, переходим к следующей
    def next_key():
        global qte_word, next_k
        qte_word = qte_word[1:]
        next_k = ""
        if qte_word:
            next_k = qte_word[0]
        renpy.restart_interaction()
    NextKey = renpy.curry(next_key)
    qteInit = renpy.curry(qte_init)

# сам экран игры
screen scr_qte(word="", time=5.0, length=5):
    # инициализация
    on 'show' action qteInit(word, time, length)
    modal True
    if qte_word:
        # уменьшаем время, отведенное на игру, и проверяем, не вышло ли оно - проигрыш
        timer 0.01 repeat True action [SetVariable("qteTime", qteTime - .01), If(qteTime <= .0, true=Return(False))]
        # отображаем, какую кнопку нужно нажать
        text next_k.upper() align(.5, .5) size 96
        # если что-то нужно нажать, то опрашивает клавиатуру
        if len(next_k) == 1:
            key next_k action NextKey()
    else:
        # все кнопки нажаты - победа
        timer .1 action Return(True)
    # шкала времени
    bar value StaticValue(qteTime, qteMaxTime) align(.5, .1) xmaximum 600
