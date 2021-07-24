# write your code here
import random
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class FlashCard(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    boxnumber = Column(Integer)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


class Catalog:
    def __init__(self, session_):
        self.session_ = session_

    def add_card(self, q_, a_):
        new_data = FlashCard(question=q_, answer=a_, boxnumber=1)
        self.session_.add(new_data)
        self.session_.commit()

    def delete_card(self, q_):
        card_ = self.get_card(q_)
        print(card_)
        session.delete(card_)
        session.commit()

    def update_card(self, key_, q_, a_):
        card_ = self.get_card(key_)
        card_.question = q_
        card_.answer = a_
        card_.boxnumber = 1
        session.commit()

    def update_box(self, key_, value_):
        card_ = self.get_card(key_)
        new_number = card_.boxnumber + 1
        if value_ == -1:
            new_number = 1
        card_.boxnumber = new_number
        session.commit()

    def get_card(self, q_):
        return self.session_.query(FlashCard).filter(FlashCard.question == q_).all()[0]

    def get_cards(self):
        result_list = self.session_.query(FlashCard).all()
        cards_ = {}
        for result_ in result_list:
            cards_.update({result_.question: result_.answer})
        return cards_

    def clear_box(self):
        result_list = self.session_.query(FlashCard).all()
        for result_ in result_list:
            if result_.boxnumber > 2:
                self.delete_card(result_.question)


class FlashCardService:
    def __init__(self, catalog_):
        self.catalog_ = catalog_

    def save_card(self):
        q_, a_ = "", ""
        while True:
            print("Question:")
            q_ = input()
            if q_.strip() == "":
                continue
            break
        while True:
            print("Answer:")
            a_ = input()
            if a_.strip() == "":
                continue
            break
        self.catalog_.add_card(q_, a_)

    def get_card(self):
        return self.catalog_.get_cards()

    def delete_card(self, key_):
        self.catalog_.delete_card(key_)

    def update_card(self, key_):
        card_ = self.catalog_.get_card(key_)
        print("current question: {}".format(card_.question))
        while True:
            print("please write a new question:")
            q_ = input()
            if q_.strip() == "":
                continue
            break
        print("current answer: {}".format(card_.answer))
        while True:
            print("please write a new answer:")
            a_ = input()
            if a_.strip() == "":
                continue
            break
        self.catalog_.update_card(key_, q_, a_)

    def clear_box(self):
        self.catalog_.clear_box()

    def update_box(self, key_):
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        choice_ = input()
        if choice_ == "y":
            self.catalog_.update_box(key_, 1)
        if choice_ == "n":
            self.catalog_.update_box(key_, -1)



def add_menu():
    global service
    while True:
        print("1. Add a new flashcard")
        print("2. Exit")
        choice_ = input()
        if choice_ == "1":
            service.save_card()
        elif choice_ == "2":
            break
        else:
            print("{} is not an option".format(choice_))


def practice_menu():
    global service
    cards_ = service.get_card()
    if len(cards_) == 0:
        print("There is no flashcard to practice!")
        return
    for key_, value_ in cards_.items():
        print("Question: {}".format(key_))
        print('press "y" to see the answer:')
        print('press "n" to skip:')
        print('press "u" to update:')
        choice_ = input()
        print()
        if choice_ == "y":
            print("Answer: {}".format(value_))
            print()
            service.update_box(key_)
            continue
        if choice_ == "u":
            update_menu(key_)
            print()
            continue
        if choice_ == "n":
            service.update_box(key_)
            continue
        print("{} is not a option".format(choice_))
    service.clear_box()


def update_menu(key_):
    print('press "d" to delete the flashcard:')
    print('press "e" to edit the flashcard:')
    choice_ = input()
    if choice_ == "d":
        service.delete_card(key_)
    if choice_ == "e":
        service.update_card(key_)
        print()


def main_menu():
    while True:
        print("1. Add flashcards")
        print("2. Practice flashcards")
        print("3. Exit")
        choice_ = input()
        if choice_ == "1":
            add_menu()
        elif choice_ == "2":
            practice_menu()
        elif choice_ == "3":
            print("Bye!")
            break
        else:
            print("{} is not an option".format(choice_))


catalog = Catalog(session)
service = FlashCardService(catalog)
main_menu()
