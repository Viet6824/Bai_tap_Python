import random
import tkinter as tk
from tkinter import messagebox

# Lớp đại diện cho lá bài
class BJ_Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def get_vietnamese_name(self):
        rank_map = {
            "Ace": "Át", "2": "2", "3": "3", "4": "4", "5": "5",
            "6": "6", "7": "7", "8": "8", "9": "9", "10": "10",
            "Jack": "J", "Queen": "Q", "King": "K"
        }
        suit_map = {
            "Hearts": "❤️", "Diamonds": "♦️", "Clubs": "♣️", "Spades": "♠️"
        }
        return f"{rank_map.get(self.value, self.value)}{suit_map.get(self.suit, '')}"

# Lớp đại diện cho bộ bài
class BJ_Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.cards = [BJ_Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    def deal(self):
        if self.cards:
            return [self.cards.pop()]
        return None

# Lớp đại diện cho tay bài
class BJ_Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.value == "Ace":
                value += 11
                aces += 1
            elif card.value in ["Jack", "Queen", "King"]:
                value += 10
            else:
                value += int(card.value) if card.value.isdigit() else 0
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def get_vietnamese_string(self):
        return ",".join(card.get_vietnamese_name() for card in self.cards)

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21

# Lớp quản lý trò chơi
class BJ_Game:
    def __init__(self):
        self.deck = BJ_Deck()
        self.player_hand = BJ_Hand()
        self.dealer_hand = BJ_Hand()

    def initial_deal(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal()[0])
            self.dealer_hand.add_card(self.deck.deal()[0])

    def hit(self):
        card = self.deck.deal()
        if card:
            self.player_hand.add_card(card[0])

    def dealer_play(self):
        while self.dealer_hand.get_value() < 17:
            card = self.deck.deal()
            if card:
                self.dealer_hand.add_card(card[0])
        return self.dealer_hand.get_value()

# Giao diện 
class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.game = BJ_Game()

        # người chơi
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)
        self.player_label = tk.Label(self.player_frame, text="Player:", font=("Arial", 14))
        self.player_label.pack()
        self.player_cards = tk.Label(self.player_frame, text="", font=("Arial", 12))
        self.player_cards.pack()
        self.player_score = tk.Label(self.player_frame, text="Score: 0", font=("Arial", 12))
        self.player_score.pack()

        # dealer
        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.pack(pady=10)
        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer:", font=("Arial", 14))
        self.dealer_label.pack()
        self.dealer_cards = tk.Label(self.dealer_frame, text="", font=("Arial", 12))
        self.dealer_cards.pack()
        self.dealer_score = tk.Label(self.dealer_frame, text="Score: ?", font=("Arial", 12))
        self.dealer_score.pack()

        # nút
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)
        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, font=("Arial", 12))
        self.hit_button.pack(side=tk.LEFT, padx=5)
        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, font=("Arial", 12))
        self.stand_button.pack(side=tk.LEFT, padx=5)
        self.new_game_button = tk.Button(self.button_frame, text="New Game", command=self.new_game, font=("Arial", 12))
        self.new_game_button.pack(side=tk.LEFT, padx=5)

        # Label kết quả
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.new_game()

    def new_game(self):
        self.game = BJ_Game()
        self.game.initial_deal()
        self.update_display()
        if self.game.dealer_hand.is_blackjack():
            self.update_display(show_dealer=True)
            self.result_label.config(text="Dealer Blackjack! You lose.")
            messagebox.showinfo("Result", "Dealer Blackjack! You lose.")
            self.end_game()
        elif self.game.player_hand.is_blackjack():
            self.update_display(show_dealer=True)
            self.result_label.config(text="Blackjack!")
            messagebox.showinfo("Result", "Blackjack!")
            self.end_game()
        else:
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.result_label.config(text="")

    def update_display(self, show_dealer=False):
        self.player_cards.config(text=self.game.player_hand.get_vietnamese_string())
        self.player_score.config(text=f"Score: {self.game.player_hand.get_value()}")
        if show_dealer:
            self.dealer_cards.config(text=self.game.dealer_hand.get_vietnamese_string())
            self.dealer_score.config(text=f"Score: {self.game.dealer_hand.get_value()}")
        else:
            if self.game.dealer_hand.cards:
                first_card = self.game.dealer_hand.cards[0].get_vietnamese_name()
                hidden_cards = ",".join("?" for _ in range(len(self.game.dealer_hand.cards) - 1))
                self.dealer_cards.config(text=f"{first_card},{hidden_cards}" if hidden_cards else first_card)
                self.dealer_score.config(text="Score: ?")

    def hit(self):
        self.game.hit()
        self.update_display()
        if self.game.player_hand.get_value() > 21:
            self.result_label.config(text="Over 21! You lose.")
            messagebox.showinfo("Result", "Over 21! You lose.")
            self.end_game()
        elif self.game.player_hand.is_blackjack():
            self.result_label.config(text="Blackjack!")
            messagebox.showinfo("Result", "Blackjack!")
            self.end_game()

    def stand(self):
        dealer_value = self.game.dealer_play()
        self.update_display(show_dealer=True)
        player_value = self.game.player_hand.get_value()
        if dealer_value > 21:
            self.result_label.config(text="Dealer over 21! You win!")
            messagebox.showinfo("Result", "Dealer over 21! You win!")
        elif dealer_value > player_value:
            self.result_label.config(text="Dealer wins!")
            messagebox.showinfo("Result", "Dealer wins!")
        elif player_value > dealer_value:
            self.result_label.config(text="You win!")
            messagebox.showinfo("Result", "You win!")
        else:
            self.result_label.config(text="Tie!")
            messagebox.showinfo("Result", "Tie!")
        self.end_game()

    def end_game(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

# Chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()