from sqlalchemy.orm import Session
from models.database import engine
from models.cards import Cards


def add_to_db(title, link, date, city, beds, description, price):
    with Session(engine) as session:
        card = Cards(title=title, link=link, date=date, city=city, beds=beds, description=description, price=price)
        session.add(card)
        session.commit()

if __name__ == '__main__':
    new_card = Cards(title='title', link='http', date='07-09-2022', city='Kiev', beds=2, description='Good',
                     price=2120.00)
    add_to_db(new_card)