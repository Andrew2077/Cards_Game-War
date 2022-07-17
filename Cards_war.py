from re import S
from PyQt5.QtWidgets import QMainWindow, QApplication,QLabel,QPushButton,QMessageBox
from PyQt5.QtGui import QPixmap,QFont,QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from sys import argv
import random

class Cards_war(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("cards_war.ui", self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon('icons8-ace-of-hearts-100.png'))
        self.setFixedSize(self.size())
        self.setWindowTitle("cards war")
        
        self.player1_card = self.findChild(QLabel, "label")
        self.player2_card = self.findChild(QLabel, "label_2")
        self.game_status = self.findChild(QLabel, "label_3")
        self.player1_info = self.findChild(QLabel, "label_4")
        self.player2_info = self.findChild(QLabel, "label_5")
        self.deal_button = self.findChild(QPushButton, "pushButton")
        self.rest_button = self.findChild(QPushButton, "pushButton_2")
        
        self.deal_button.clicked.connect(self.deal)
        self.rest_button.clicked.connect(self.rest)

        self.card_type = ['diamonds', 'clubs', 'hearts', 'spades']
        self.all_card = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king','ace',]
        self.deck = {}
        for type in self.card_type:
            value = 2
            for card in self.all_card:
                
                #self.deck.append(type + '_' + card)
                self.deck[type + '_' + card] = value
                value+=1
                
        self.deck_original = self.deck.copy()     #*save the original deck
        self.deck = self.suffeling_dec(self.deck)  #*shuffle the deck
        
        self.player1_deck = dict(zip(list(self.deck.keys())[:len(self.deck)//2], list(self.deck.values())))
        self.player2_deck = dict(zip(list(self.deck.keys())[len(self.deck)//2:], list(self.deck.values())[len(self.deck)//2:]))
        
        self.player1_score = 0
        self.player2_score = 0
          
        self.card_back = 'blue'
        self.cardback = QPixmap(f'fronts/{self.card_back}.svg')
        
        self.player1_card.setPixmap(self.cardback)
        self.player2_card.setPixmap(self.cardback)
        #self.player2_card.setPixmap(QPixmap(f'Cards Deck/svg_playing_cards/fronts/{self.deck[0]}.svg'))
        self.card = ''
        
        self.statusbar.setFont(QFont("Arial", 12, QFont.Bold))
        self.statusbar.showMessage(f"Game started {len(self.player1_deck)} cards left")
        
        
        self.show()
    
    def suffeling_dec(self, deck):  #* shuffeling using Keys
        self.decK_keys = list(deck.keys())
        random.shuffle(self.decK_keys)
        #return [(key, d[key]) for key in self.decK_keys]
        self.suffled_values = []
        for key in self.decK_keys:
            if key in self.deck_original:
                self.suffled_values.append(self.deck_original[key])
                
        #print(dict(zip(self.decK_keys, self.suffled_values)))
        return dict(zip(self.decK_keys, self.suffled_values))
        
    
    def check_score(self):
        # print(self.player1_deck)
        # print(self.player2_deck)
        self.player1_Picked_card = list(self.player1_deck.keys())[0]
            
        self.player2_Picked_card = list(self.player2_deck.keys())[0]
        self.player1_card_value = int(self.player1_deck[self.player1_Picked_card])
        del self.player1_deck[self.player1_Picked_card]
        
        self.player2_card_value = int(self.player2_deck[self.player2_Picked_card])
        del self.player2_deck[self.player2_Picked_card]
        
        if self.player1_card_value > self.player2_card_value:
            self.player1_score += 1
            self.game_status.setText(f"Player 1 wins the round")
            self.player1_info.setText(f"Player 1 score: {self.player1_score}")
        
        elif self.player1_card_value < self.player2_card_value:
            self.player2_score += 1
            self.game_status.setText(f"Player 2 wins the round")
            self.player2_info.setText(f"Player 2 score: {self.player2_score}")
            
        elif self.player1_card_value == self.player2_card_value:
            self.game_status.setText("Tie")
            

            
    
    def deal(self):
        # try:
            self.check_score()
            #self.deck.clear()
            self.statusbar.showMessage(f"{len(self.player1_deck)} cards left")
            self.player1_card.setPixmap(QPixmap(f'fronts/{self.player1_Picked_card}.svg'))
            self.player2_card.setPixmap(QPixmap(f'fronts/{self.player2_Picked_card}.svg'))
            
            if len(self.player1_deck) == 0:
                
                self.rest_button.setEnabled(True)
                self.deal_button.setEnabled(False)
            
            
        # except Exception as e:       
                msg = QMessageBox()
                msg.setWindowTitle("Game Over")
                
                if self.player1_score > self.player2_score:
                    self.statusbar.showMessage(f"Player 1 won the game with score {self.player1_score}")
                    msg.setText("Player 1 won the game")
                elif self.player1_score < self.player2_score:
                    self.statusbar.showMessage(f"Player 2 won the game with score {self.player2_score}")
                    msg.setText("Player 2 won the game")
                elif self.player1_score == self.player2_score:
                    self.statusbar.showMessage(f"Tie with score {self.player1_score}")
                    msg.setText("Tie")
                    
                msg.setWindowIcon(QIcon("question.png"))
                #msg.setIcon(QMessageBox.information)
                msg.setInformativeText("Do you want to play again?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                # msg.setStandardButtons(QMessageBox.Close | QMessageBox.Reset | QMessageBox.Cancel)
                # msg.setDefaultButton(QMessageBox.Reset)
                msg.setStyleSheet("background-color: rgb(255,255,255)")
                ret = msg.exec()
                if ret == QMessageBox.Yes:
                    self.rest()
                elif ret == QMessageBox.No:
                    app.exit()    
            
        #     # msg_box = QMessageBox()
        #     # #change the color of the message box
        #     # msg_box.setStyleSheet("background-color: rgb(0, 0, 0);")
        #     # msg_box.setStyleSheet("background-color: rgb(211,211,211);")
        #     # msg_box.warning(self, "Error", "Please select a language")     
        #     #msg_box.about(self, "Error", str(e))
            
        
        
        #print(self.deck)
    def rest(self):
        self.deal_button.setEnabled(True)
        self.deck_original = self.deck.copy()  
        self.deck = self.suffeling_dec(self.deck) 
        self.player1_deck = dict(zip(list(self.deck.keys())[:len(self.deck)//2], list(self.deck.values())))
        self.player2_deck = dict(zip(list(self.deck.keys())[len(self.deck)//2:], list(self.deck.values())[len(self.deck)//2:]))
        self.player1_score = 0
        self.player2_score = 0
        self.player1_card.setPixmap(self.cardback)
        self.player2_card.setPixmap(self.cardback)
        self.game_status.setText(f"Deal cards to start")
        self.player1_info.setText(f"Player 1 score: {self.player1_score}")
        self.player2_info.setText(f"Player 2 score: {self.player2_score}")
        self.statusbar.showMessage(f"Game started {len(self.player1_deck)} cards left")



app = QApplication(argv)
mainWindow = Cards_war()
app.exec_()
