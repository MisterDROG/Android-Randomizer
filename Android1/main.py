__version__ = '0.9.1'

import os

from kivy.config import Config

Config.set('graphics', 'resizable', 1)

import random
import sys
from pprint import pprint

import gameBBG_docs

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown


Window.size = (326, 689)

#Window.fullscreen = 'auto'

class BGPopup(Popup):

    def __init__(self, picture, c1, c2, c3, c4, **kwargs):
        # make sure we aren't overriding any important functionality
        super(BGPopup, self).__init__(**kwargs)

        with self.canvas.before:
            Color(c1, c2, c3, c4)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos, source=picture)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class SpinnerOptions(SpinnerOption):

    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0.35, 0, 0, 1]
        self.bold = True
        self.color = [1, 1, 1, 1]
        self.height = Window.size[1] * .1


class SpinnerDropdown(DropDown):

    def __init__(self, **kwargs):
        super(SpinnerDropdown, self).__init__(**kwargs)
        self.auto_width = True
        #self.width = 150


class SpinnerWidget(Spinner):
    def __init__(self, **kwargs):
        super(SpinnerWidget, self).__init__(**kwargs)
        self.dropdown_cls = SpinnerDropdown
        self.option_cls = SpinnerOptions


class BGGridLayout(GridLayout):

    def __init__(self, picture, c1, c2, c3, c4, **kwargs):
        # make sure we aren't overriding any important functionality
        super(BGGridLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(c1, c2, c3, c4)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos, source=picture)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MyApp(App):
    def __init__(self):
        super().__init__()
        self.basic_labels = list(gameBBG_docs.labels_season1)
        self.basic_phrases = list(gameBBG_docs.phrases_season1)
        self.sm = ScreenManager()
        self.players = 0
        self.rounds = 0
        self.game_stack = []
        self.players_tec = -1
        self.rounds_tec = 1
        self.labels_stack = []
        self.phrases_stack = []

    def close_app(self, instance):
        path_label = os.path.abspath("labels_act.txt")
        path_phrase = os.path.abspath("phrase_act.txt")
        if os.path.exists(path_label):
            os.remove(path_label)
        if os.path.exists(path_phrase):
            os.remove(path_phrase)
        with open(path_label, 'w', encoding='utf-8') as file:
            for label in self.labels_stack:
                file.write(label+'\n')
        print('записана длина лейблов:', len(self.labels_stack))
        with open(path_phrase, 'w', encoding='utf-8') as file:
            for phrase in self.phrases_stack:
                file.write(phrase+'\n')
        print('записана длина фраз:', len(self.phrases_stack))
        sys.exit()

    def help(self, instance):
        self.sm.current = 'Help_screen'

    def screen_pos(self, screen):
        self.sm.current = screen

    def main_page(self, instance):
        self.players_tec = -1
        self.rounds_tec = 1
        self.game_stack = []
        self.sm.current = 'Main_screen'

    def game_settings(self, instance):
        self.sm.current = 'Settings_screen'

    def all_settings(self, instance):
        self.sm.current = 'All_settings_screen'

    def game_builder(self):
        self.game_stack = []
        if self.labels_stack == [] or len(self.labels_stack) < self.players:
            self.labels_stack = list(self.basic_labels)
        if self.phrases_stack == [] or len(self.phrases_stack) < (self.rounds * self.players):
            self.phrases_stack = list(self.basic_phrases)
        random.shuffle(self.labels_stack)
        random.shuffle(self.phrases_stack)
        print(len(self.labels_stack), len(self.basic_labels))
        print(len(self.phrases_stack), len(self.basic_phrases))
        for player in range(self.players):
            self.game_stack.append([self.labels_stack.pop(), ])
        print(self.game_stack)
        i = 0
        print(len(self.labels_stack), len(self.basic_labels))
        for player in self.game_stack:
            for rounds in range(self.rounds):
                self.game_stack[i].append(self.phrases_stack.pop())
            i += 1
        print(len(self.phrases_stack), len(self.basic_phrases))
        pprint(self.game_stack)

        path_label = os.path.abspath("labels_act.txt")
        path_phrase = os.path.abspath("phrase_act.txt")
        if os.path.exists(path_label):
            os.remove(path_label)
        if os.path.exists(path_phrase):
            os.remove(path_phrase)
        with open(path_label, 'w', encoding='utf-8') as file:
            for label in self.labels_stack:
                file.write(label+'\n')
        print('записана длина лейблов:', len(self.labels_stack))
        with open(path_phrase, 'w', encoding='utf-8') as file:
            for phrase in self.phrases_stack:
                file.write(phrase+'\n')
        print('записана длина фраз:', len(self.phrases_stack))

    def start_game(self, instance):
        if self.players == 0 or self.rounds == 0:
            pass
        else:
            self.game_builder()
            self.sm.current = 'Game_screen'

    def on_text_players(self, instance, value):
        if value == '':
            value = 0
        self.players = int(value)
        return int(value)

    def on_text_rounds(self, instance, value):
        if value == '':
            value = 0
        self.rounds = int(value)
        return int(value)

    def label_restart(self, instance):
        self.labels_stack = list(self.basic_labels)
        print(len(self.labels_stack), len(self.basic_labels))
        print(len(self.phrases_stack), len(self.basic_phrases))

    def phrase_restart(self, instance):
        self.phrases_stack = list(self.basic_phrases)
        print(len(self.labels_stack), len(self.basic_labels))
        print(len(self.phrases_stack), len(self.basic_phrases))

    def build(self):

        path_label = os.path.abspath("labels_act.txt")
        path_phrase = os.path.abspath("phrase_act.txt")
        with open(path_label, 'r', encoding='utf-8') as file:
            for label in file:
                label = label.replace("\n","")
                self.labels_stack.append(label)
        print('длина лейблов:', len(self.labels_stack))
        with open(path_phrase, 'r', encoding='utf-8') as file:
            for phrase in file:
                phrase = phrase.replace("\n", "")
                self.phrases_stack.append(phrase)
        print('длина фраз:', len(self.phrases_stack))

        screen_main = Screen(name='Main_screen')
        self.sm.add_widget(screen_main)
        screen_help = Screen(name='Help_screen')
        self.sm.add_widget(screen_help)
        screen_all_settings = Screen(name='All_settings_screen')
        self.sm.add_widget(screen_all_settings)
        screen_settings = Screen(name='Settings_screen')
        self.sm.add_widget(screen_settings)
        screen_game = Screen(name='Game_screen')
        self.sm.add_widget(screen_game)

        ''' Main_Screen'''

        gl_main = BGGridLayout(rows=2, picture='Light.jpg', c1=1, c2=0, c3=0, c4=1)
        screen_main.add_widget(gl_main)

        gl_up = GridLayout(rows=1)
        gl_down = GridLayout(rows=4, padding=35, spacing=0)

        gl_main.add_widget(gl_up)
        gl_main.add_widget(gl_down)

        bt_ng = Button(text='НОВАЯ ИГРА',
                       # border=(10, 10, 10, 10),
                       bold=True,
                       background_color=(1, .0, .0, 1),
                       background_normal='Plate_bt.jpg',
                       on_press=self.game_settings)
        bt_help = Button(text='ПРАВИЛА',
                         bold=True,
                         background_color=(1, .0, .0, 1),
                         background_normal='Plate_bt.jpg',
                         on_press=self.help)
        bt_all_settings = Button(text='НАСТРОЙКИ',
                                 bold=True,
                                 background_color=(1, .0, .0, 1),
                                 background_normal='Plate_bt.jpg',
                                 on_press=self.all_settings)
        bt_out = Button(text='ВЫХОД',
                        bold=True,
                        background_color=(1, .0, .0, 1),
                        background_normal='Plate_bt.jpg',
                        on_press=self.close_app)

        gl_down.add_widget(bt_ng)
        gl_down.add_widget(bt_help)
        gl_down.add_widget(bt_all_settings)
        gl_down.add_widget(bt_out)

        name_label = Label(text='BEST GAME',
                           color=(0, 0, 0, 1),
                           text_size=(Window.size[0] * 0.7, Window.size[1] * 0.55),
                           font_size=Window.size[1] * .1,
                           # font_size='60sp',
                           bold=True,
                           halign='center',
                           valign='bottom')

        gl_up.add_widget(name_label)

        ''' Help_Screen'''

        gl_help = BGGridLayout(rows=3, padding=35, spacing=3, picture='Wall2.jpg', c1=0.3, c2=0.3, c3=0.3, c4=1)
        screen_help.add_widget(gl_help)
        help_label = Label(text='ПРАВИЛА',
                           text_size=(Window.size[0] * 0.8, None),
                           font_size=Window.size[1] * .07,
                           bold=True,
                           halign='center',
                           valign='middle',
                           size_hint=(1, .1))
        gl_help.add_widget(help_label)
        help_text_label = Label(text=gameBBG_docs.game_rules,
                                text_size=(Window.size[0] * 0.9, None),
                                font_size=Window.size[1] * .021,
                                halign='center',
                                valign='middle')
        gl_help.add_widget(help_text_label)
        bt_main_help = Button(text='ГЛАВНОЕ МЕНЮ',
                              bold=True,
                              background_color=(1, .0, .0, 1),
                              background_normal='Plate_bt.jpg',
                              on_press=self.main_page,
                              size_hint=(1, .15))
        gl_help.add_widget(bt_main_help)

        ''' All_settings_Screen'''

        gl_all_settings = BGGridLayout(rows=6, padding=35, spacing=3, picture='Wall2.jpg', c1=0.3, c2=0.3, c3=0.3, c4=1)
        screen_all_settings.add_widget(gl_all_settings)
        all_settings_label = Label(text='НАСТРОЙКИ',
                                   text_size=(Window.size[0] * 0.8, None),
                                   font_size=Window.size[1] * .06,
                                   bold=True,
                                   halign='center',
                                   valign='middle',
                                   size_hint=(1, .3))
        gl_all_settings.add_widget(all_settings_label)

        spinner = SpinnerWidget(
            text='СЕЗОН',
            values=('СЕЗОН 1: Транспорт', 'СЕЗОН 2: Еда', 'СЕЗОН 3: Животные'),
            size_hint=(1, .1),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5},
            bold=True,
            background_color=(1, .0, .0, 1),
            background_normal='Plate_bt.jpg')

        def selected_value(spinner, text):
            if text == 'СЕЗОН 1: Транспорт':
                self.basic_labels = list(gameBBG_docs.labels_season1)
                self.basic_phrases = list(gameBBG_docs.phrases_season1)
                self.labels_stack = list(self.basic_labels)
                self.phrases_stack = list(self.basic_phrases)
                print(self.basic_labels[0], 'Сменили на: СЕЗОН 1: Транспорт')
            elif text == 'СЕЗОН 2: Еда':
                self.basic_labels = list(gameBBG_docs.labels_season2)
                self.basic_phrases = list(gameBBG_docs.phrases_season2)
                self.labels_stack = list(self.basic_labels)
                self.phrases_stack = list(self.basic_phrases)
                print(self.basic_labels[0], 'Сменили на: СЕЗОН 2: Еда')
            elif text == 'СЕЗОН 3: Животные':
                self.basic_labels = list(gameBBG_docs.labels_season3)
                self.basic_phrases = list(gameBBG_docs.phrases_season3)
                self.labels_stack = list(self.basic_labels)
                self.phrases_stack = list(self.basic_phrases)
                print(self.basic_labels[0], 'Сменили на: СЕЗОН 3: Животные')

        spinner.bind(text=selected_value)
        gl_all_settings.add_widget(spinner)

        def change_status(btn, text):
            btn.text = text

        bt_label_shuffle = Button(text='Перемешать Лейблы',
                                  bold=True,
                                  background_color=(1, .0, .0, 1),
                                  background_normal='Plate_bt.jpg',
                                  on_press=self.label_restart,
                                  size_hint=(1, .1))
        bt_label_shuffle.bind(on_press=lambda x: change_status(btn=bt_label_shuffle, text='Перемешать Лейблы: Готово'))
        gl_all_settings.add_widget(bt_label_shuffle)

        bt_phrase_shuffle = Button(text='Перемешать Фразы',
                                   bold=True,
                                   background_color=(1, .0, .0, 1),
                                   background_normal='Plate_bt.jpg',
                                   on_press=self.phrase_restart,
                                   size_hint=(1, .1))
        bt_phrase_shuffle.bind(on_press=lambda x: change_status(btn=bt_phrase_shuffle, text='Перемешать Фразы: Готово'))
        gl_all_settings.add_widget(bt_phrase_shuffle)

        def about_game(instance):
            label_ab = Label(text=gameBBG_docs.game_about,
                             halign='center',
                             valign='middle')
            popup_ab = Popup(title='BEST GAME',
                             content=label_ab,
                             separator_height=0,
                             title_align='center',
                             background_color=(0.8, 0, 0, 1),
                             size_hint=(.7, .3))
            popup_ab.open()

        bt_unused = Button(text='ОБ ИГРЕ',
                           bold=True,
                           background_color=(1, .0, .0, 1),
                           background_normal='Plate_bt.jpg',
                           on_press=about_game,
                           size_hint=(1, .1))
        gl_all_settings.add_widget(bt_unused)

        bt_main_help = Button(text='ГЛАВНОЕ МЕНЮ',
                              bold=True,
                              background_color=(1, .0, .0, 1),
                              background_normal='Plate_bt.jpg',
                              on_press=self.main_page,
                              size_hint=(1, .1))
        gl_all_settings.add_widget(bt_main_help)

        ''' Settings_Screen'''
        gl_settings = BGGridLayout(rows=7, padding=35, spacing=3, picture='Wall2.jpg', c1=0.3, c2=0.3, c3=0.3, c4=1)
        screen_settings.add_widget(gl_settings)

        settings_label = Label(text='НОВАЯ ИГРА',
                               text_size=(Window.size[0] * 0.8, None),
                               font_size=Window.size[1] * .06,
                               bold=True,
                               halign='center',
                               valign='middle',
                               size_hint=(1, .1))
        gl_settings.add_widget(settings_label)

        num_players_label = Label(text='Введите число игроков:',
                                  text_size=(Window.size[0] * 0.8, None),
                                  font_size=Window.size[1] * .04,
                                  bold=False,
                                  halign='center',
                                  valign='middle',
                                  size_hint=(1, .2))
        gl_settings.add_widget(num_players_label)

        num_players_input = TextInput(halign='center',
                                      font_size=Window.size[1] * .07,
                                      size_hint=(1, .1))
        num_players_input.bind(text=self.on_text_players)
        gl_settings.add_widget(num_players_input)

        num_rounds_label = Label(text='Введите число раундов:',
                                 text_size=(Window.size[0] * 0.8, None),
                                 font_size=Window.size[1] * .04,
                                 bold=False,
                                 halign='center',
                                 valign='middle',
                                 size_hint=(1, .2))
        gl_settings.add_widget(num_rounds_label)

        num_rounds_input = TextInput(halign='center',
                                     font_size=Window.size[1] * .07,
                                     size_hint=(1, .1))
        num_rounds_input.bind(text=self.on_text_rounds)
        gl_settings.add_widget(num_rounds_input)

        bt_set_ready = Button(text='ГОТОВО',
                              bold=True,
                              background_color=(1, .0, .0, 1),
                              background_normal='Plate_bt.jpg',
                              on_press=self.start_game,
                              size_hint=(1, .1))
        bt_set_ready.bind(on_press=lambda x: change_status(btn=bt_label_shuffle, text='Перемешать Лейблы'))
        bt_set_ready.bind(on_press=lambda x: change_status(btn=bt_phrase_shuffle, text='Перемешать Фразы'))
        gl_settings.add_widget(bt_set_ready)

        bt_main_help2 = Button(text='ГЛАВНОЕ МЕНЮ',
                               bold=True,
                               background_color=(1, .0, .0, 1),
                               background_normal='Plate_bt.jpg',
                               on_press=self.main_page,
                               size_hint=(1, .1))
        gl_settings.add_widget(bt_main_help2)

        ''' Game_Screen'''

        gl_game = BGGridLayout(rows=6, padding=35, spacing=3, picture='Wall2.jpg', c1=0.3, c2=0.3, c3=0.3, c4=1)
        screen_game.add_widget(gl_game)

        round_label = Label(text='ИГРОКАМ ПРИГОТОВИТЬСЯ',
                            size_hint=(1, .1),
                            text_size=(Window.size[0] * 0.8, None),
                            font_size=Window.size[1] * .04,
                            bold=True,
                            halign='center',
                            valign='middle')
        gl_game.add_widget(round_label)

        num_gamer_label = Label(text='(ИГРОК)',
                                size_hint=(1, .1),
                                text_size=(Window.size[0] * 0.8, None),
                                font_size=Window.size[1] * .035,
                                bold=False,
                                halign='center',
                                valign='middle')
        gl_game.add_widget(num_gamer_label)

        vash_phras_label = Label(text='ВАША ФРАЗА:',
                                 size_hint=(1, .1),
                                 text_size=(Window.size[0] * 0.8, None),
                                 font_size=Window.size[1] * .04,
                                 bold=True,
                                 halign='center',
                                 valign='middle')
        gl_game.add_widget(vash_phras_label)

        phrasа_label = Label(text='(ФРАЗА)',
                             size_hint=(1, .4),
                             text_size=(Window.size[0] * 0.8, None),
                             font_size=Window.size[1] * .035,
                             bold=False,
                             halign='center',
                             valign='middle')
        gl_game.add_widget(phrasа_label)

        def main_page_ingame(instanse):
            self.players_tec = -1
            self.rounds_tec = 1
            self.game_stack = []
            self.sm.current = 'Main_screen'
            num_gamer_label.text = '(ИГРОК)'
            round_label.text = 'ИГРОКАМ ПРИГОТОВИТЬСЯ'
            phrasа_label.text = '(ФРАЗА)'

        def zamena(instance):
            print('начало', self.players_tec, self.rounds_tec, 'всего', self.players, self.rounds)
            if self.players_tec == (self.players - 1) and self.rounds_tec == (self.rounds):
                self.players_tec = -1
                self.rounds_tec = 1

                bt_cl_pu = Button(text='НА ГЛАВНУЮ',
                                  on_press=main_page_ingame,
                                  background_color=(1, .0, .0, 1),
                                  bold=True
                                  )
                popup = Popup(title='КОНЕЦ ИГРЫ - РАСХОДИМСЯ!',
                              content=bt_cl_pu,
                              separator_height=0,
                              title_align='center',
                              background_color=(0.5, 0.5, 0.5, 1),
                              size_hint=(.5, .2),
                              auto_dismiss=False)

                bt_cl_pu.bind(on_press=popup.dismiss)
                popup.open()
            else:
                if self.players_tec < (self.players - 1):
                    self.players_tec += 1
                else:
                    self.rounds_tec += 1
                    self.players_tec = 0
                print(self.players_tec, self.rounds_tec, 'всего', self.players, self.rounds)
                num_gamer_label.text = 'Игрок ' + str(self.players_tec + 1) + ': ' + self.game_stack[self.players_tec][
                    0]
                round_label.text = 'РАУНД ' + str(self.rounds_tec)
                phrasа_label.text = self.game_stack[self.players_tec][self.rounds_tec]
                print(self.game_stack[self.players_tec][self.rounds_tec])
                # bt_sled_ig.text = 'СЛЕДУЮЩИЙ ИГРОК ' + str(self.players_tec + 2) + ': ' + str(self.game_stack[self.players_tec+1][0])

        bt_sled_ig = Button(text='СЛЕДУЮЩИЙ',
                            bold=True,
                            background_color=(1, .0, .0, 1),
                            background_normal='Plate_bt.jpg',
                            size_hint=(1, .1), )
        bt_sled_ig.bind(on_press=zamena)
        gl_game.add_widget(bt_sled_ig)

        def main_page_q(instance):
            bt_cl_pu_q = Button(text='ДА!',
                                on_press=main_page_ingame,
                                background_color=(1, .0, .0, 1),
                                bold=True
                                )
            popup_q = Popup(title='ПРЯМ ВЫХОДИМ?',
                            content=bt_cl_pu_q,
                            separator_height=0,
                            title_align='center',
                            background_color=(0.5, 0.5, 0.5, 1),
                            size_hint=(.5, .2))

            bt_cl_pu_q.bind(on_press=popup_q.dismiss)
            popup_q.open()

        bt_main_game = Button(text='ГЛАВНОЕ МЕНЮ',
                              bold=True,
                              background_color=(1, .0, .0, 1),
                              background_normal='Plate_bt.jpg',
                              size_hint=(1, .1),
                              on_press=main_page_q)
        gl_game.add_widget(bt_main_game)

        return self.sm


if __name__ == "__main__":
    MyApp().run()
