from sqlalchemy import Column, Integer, String, Date, Numeric
from models.database import Base
from models.database import create_db


class Cards(Base):
    __tablename__ = 'cards'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(250))                      # 2 - title
    link = Column(String(300))                       # 1 - img (url)
    date = Column(Date)                              # 3 - date (dd-mm-yyyy)
    city = Column(String(300))                       # 4 - city
    beds = Column(String(50))                        # 5 - beds
    description = Column(String(5000))               # 6 - description
    price = Column(Numeric(precision=8, scale=2))    # 7 - price

    def __repr__(self):
        info: str = f'title: {self.title}\nlink: {self.link}\ndate: {self.date}\nprice: {self.price}\ncity: {self.city}\nbeds: {self.beds}\ndesc: {self.description}\n'
        return info


if __name__ == '__main__':
    create_db()

