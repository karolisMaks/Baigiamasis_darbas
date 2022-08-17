from sqlalchemy import Column, Integer, String, Float, create_engine,Date
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///biudzeto_duomenu_baze.db')
Base = declarative_base()

class Lentele(Base):
    __tablename__ = 'Biudzetas'
    id = Column(Integer, primary_key = True)
    tipas = Column('Iraso tipas', String,nullable=False)
    paskirtis = Column('Paskirtis', String,nullable=False)
    suma = Column('Suma', Float,nullable=False)
    iraso_data = Column('Iraso data', Date,nullable=False)

    def __init__(self, tipas, paskirtis, suma, iraso_data):
        self.tipas = tipas
        self.paskirtis = paskirtis
        self.suma = suma
        self.iraso_data = iraso_data

    def __repr__(self):
        return f'{self.id} {self.tipas} {self.paskirtis} {self.suma} {self.iraso_data}'
Base.metadata.create_all(engine)