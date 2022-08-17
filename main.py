from lentele import Lentele
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tkinter import *
from tkinter import ttk
import logging

#   Sukuria iraso pridejimo ir pakeitimo mygtukus
class Sukurti_mygtuka():
    def __init__(self,langas,tipas):
        self.langas = langas
        self.tipas = tipas
        if tipas == 'Prideti irasa':
            self.mygtukas = Button(self.langas, text='Prideti irasa', command=self.iraso_lango_sukurimas, bg='#b3b3b1')
            self.mygtukas.pack(expand=1, anchor=S, side=TOP)
        if tipas == 'Pakeisti irasa':
            self.mygtukas = Button(self.langas, text='Pakeisti irasa', command=self.pakeitimo_lango_sukurimas, bg='#b3b3b1')
            self.mygtukas.pack(expand=1)

    #   Sukuria nauja langa
    def iraso_lango_sukurimas(self):
        self.irasoLangas = Toplevel(self.langas)
        self.iraso_lango_objektas = Iraso_langas(self.irasoLangas)

    #   Sukuria nauja langa, jei lenteleje yra pazymetas irasas
    def pakeitimo_lango_sukurimas(self):
        if lentele.focus() != '':
            self.pakeitimoLangas = Toplevel(self.langas)
            self.pakeitimo_lango_objektas = Pakeitimo_Langas(self.pakeitimoLangas)

class Iraso_langas():
    #   Apsiraso iraso lango mygtukai
    def __init__(self, naujas_langas):
        self.naujas_langas = naujas_langas
        self.naujas_langas.iconbitmap(r'euro.ico')
        self.frame = Frame(self.naujas_langas, bg='#8a8a87')

        self.id_uzrasas = Label(self.frame, text='ID:', bg='#8a8a87')
        self.tipo_uzrasas = Label(self.frame, text='Tipas:', bg='#8a8a87')
        self.paskirties_uzrasas = Label(self.frame, text='Paskirtis:', bg='#8a8a87')
        self.sumos_uzrasas = Label(self.frame, text='Suma:', bg='#8a8a87')
        self.datos_uzrasas = Label(self.frame, text='Data (formatas: XXXX-XX-XX):', bg='#8a8a87')

        self.id_irasymas = Entry(self.frame, width=30, bg='#dededc')
        self.tipo_irasymas = ttk.Combobox(self.frame, values=['Pajamos', 'Islaidos'], width=27)
        self.paskirties_irasymas = Entry(self.frame, width=30, bg='#dededc')
        self.sumos_irasymas = Entry(self.frame, width=30, bg='#dededc')
        self.datos_irasymas = Entry(self.frame, width=30, bg='#dededc')

        self.irasyt_mygtukas = Button(self.frame, text='Irasyti', width=25, command=self.irasyti_nauja_irasa, bg='#b3b3b1')

        self.frame.pack(fill=BOTH)
        self.id_uzrasas.grid(row=0, column=0, sticky=E)
        self.id_irasymas.grid(row=0, column=1)
        self.tipo_uzrasas.grid(row=1, column=0, sticky=E)
        self.tipo_irasymas.grid(row=1, column=1)
        self.paskirties_uzrasas.grid(row=2, column=0, sticky=E)
        self.paskirties_irasymas.grid(row=2, column=1)
        self.sumos_uzrasas.grid(row=3, column=0, sticky=E)
        self.sumos_irasymas.grid(row=3, column=1)
        self.datos_uzrasas.grid(row=4, column=0, sticky=E)
        self.datos_irasymas.grid(row=4, column=1)
        self.irasyt_mygtukas.grid(row=5, column=1)

    def irasyti_nauja_irasa(self):
        #   Is irasymo lauku susikuria kintamieji
        self.id = self.id_irasymas.get()
        self.tipas = self.tipo_irasymas.get().capitalize()
        self.paskirtis = self.paskirties_irasymas.get().capitalize()
        self.suma = self.sumos_irasymas.get()
        self.data = self.datos_irasymas.get()

        try:
            self.suma = float(self.sumos_irasymas.get())
            self.data = datetime.datetime.strptime(self.datos_irasymas.get(), '%Y-%m-%d')

            #   Prideda irasa i lentele
            lentele.insert(parent='', index='end', iid=self.id, text='', values=(self.id, self.tipas, self.paskirtis, self.suma, self.data.date()))

            #   Prideda irasa i duomenu baze
            self.irasas = Lentele(self.tipas, self.paskirtis, self.suma, self.data)
            session.add(self.irasas)
            session.commit()

            # Prideda irasa i loggeri
            logging.info(f'Pridetas naujas irasas\niraso id: ({self.id}), iraso tipas: ({self.tipas}), paskirtis: ({self.paskirtis}), suma: ({self.suma}),data: ({self.data})')

            #   Atnaujina balansa, pajamas, islaidas ir isjungia pakeitimo langa
            atnaujinti_balansa_pajamas_islaidas()
            self.naujas_langas.destroy()

        except ValueError:
            self.klaida = Label(self.frame, text='Neteisingai ivesta data arba suma!', bg='#8a8a87')
            self.klaida.grid(row=6, columnspan=2)


class Pakeitimo_Langas():
    def __init__(self,naujas_langas):
        self.naujas_langas = naujas_langas
        self.naujas_langas.iconbitmap(r'euro.ico')
        self.langas = Frame(self.naujas_langas, bg='#8a8a87')

        #   Sukuria iraso langeliu pavadinimus kaireje puseje

        self.paskirtis_pav = Label(self.langas, text='Paskirtis:', bg='#8a8a87')
        self.tipas_pav = Label(self.langas, text='Tipas:', bg='#8a8a87')
        self.suma_pav = Label(self.langas, text='Suma:', bg='#8a8a87')
        self.data_pav = Label(self.langas, text='Data:', bg='#8a8a87')

        #   Sukuria iraso langelius desineje puseje su lenteleje pazymeto iraso duomenimis

        self.pasirinktas = lentele.focus()
        self.values = lentele.item(self.pasirinktas, 'values')

        self.paskirtis = Entry(self.langas, bg='#dededc')
        self.paskirtis.insert(0,self.values[2])
        self.tipas = Entry(self.langas, bg='#dededc')
        self.tipas.insert(0,self.values[1])
        self.suma = Entry(self.langas, bg='#dededc')
        self.suma.insert(0,self.values[3])
        self.data = Entry(self.langas, bg='#dededc')
        self.data.insert(0,self.values[4])

        #   Pakeitimo mygtukas

        self.pakeisti = Button(self.langas, text='Patvirtinti pakeitimus', command=self.pakeisti_irasa, bg='#b3b3b1')

        #   Supakuoja

        self.langas.pack(fill=BOTH, expand=1)

        self.tipas_pav.grid(row=0, column=0, sticky=E)
        self.paskirtis_pav.grid(row=1, column=0, sticky=E)
        self.suma_pav.grid(row=2, column=0, sticky=E)
        self.data_pav.grid(row=3, column=0, sticky=E)

        self.tipas.grid(row=0, column=1)
        self.paskirtis.grid(row=1, column=1)
        self.suma.grid(row=2, column=1)
        self.data.grid(row=3, column=1)

        self.pakeisti.grid(row=4, columnspan=2)

    def pakeisti_irasa(self):
        #   Is irasymo lauku susikuria kintamieji
        self.tipas_kint = self.tipas.get().capitalize()
        self.paskirtis_kint = self.paskirtis.get()
        self.suma_kint = self.suma.get()
        self.data_kint = self.data.get()

        try:
            #   Pakeicia irasa duomenu bazeje
            self.suma_kint = float(self.suma_kint)
            self.data_kint = datetime.datetime.strptime(self.data_kint, '%Y-%m-%d')

            keiciamas_irasas = session.query(Lentele).get(self.pasirinktas)

            keiciamas_irasas.tipas = self.tipas_kint
            keiciamas_irasas.paskirtis = self.paskirtis_kint
            keiciamas_irasas.suma = self.suma_kint
            keiciamas_irasas.iraso_data = self.data_kint

            session.commit()

            #   Pakeicia irasa lenteleje
            self.values = lentele.item(self.pasirinktas, text='', values=(self.pasirinktas, self.tipas_kint, self.paskirtis_kint, self.suma_kint, self.data_kint.date()))

            #   Prideda pakeitima i loggeri
            logging.info(f'Pakeistas irasas:({self.pasirinktas})\niraso tipas: ({self.tipas_kint}), paskirtis: ({self.paskirtis_kint}), suma: ({self.suma_kint}),data: ({self.data_kint.date()})')

            #   Atnaujina balansa, pajamas, islaidas ir isjungia pakeitimo langa
            atnaujinti_balansa_pajamas_islaidas()
            self.naujas_langas.destroy()

        except ValueError:
            klaida = Label(self.langas, text='Neteisingai ivesta data arba suma!', bg='#8a8a87')
            klaida.grid(row=5, columnspan=2)

#   Surenka visus irasus is duomenu bazes
def visi_irasai():
    irasai = session.query(Lentele).all()
    return irasai

#   Prideda visus irasus is duomenu bazes i lentele
def visi_irasai_lenteleje():
    for x in visi_irasai():
        lentele.insert(parent='', index='end', iid=x.id, text='', values=(x.id, x.tipas, x.paskirtis, x.suma, x.iraso_data))

#   Apskaiciuoja balansa
def gauti_balansa():
    balansas = 0
    for x in visi_irasai():
        if x.tipas == 'Pajamos':
            balansas += x.suma
        if x.tipas == 'Islaidos':
            balansas -= x.suma
    return balansas

#   Apskaiciuoja pajamas
def gauti_pajamas():
    pajamos = 0
    for x in visi_irasai():
        if x.tipas == 'Pajamos':
            pajamos += x.suma
    return pajamos

#   Apskaiciuoja islaidas
def gauti_islaidas():
    islaidos = 0
    for x in visi_irasai():
        if x.tipas =='Islaidos':
            islaidos += x.suma
    return islaidos

#   Atnaujina balansa, pajamas ir islaidas
def atnaujinti_balansa_pajamas_islaidas():
    balanso_uzrasas['text'] = f'Balansas:\n\n{gauti_balansa()}€'
    pajamu_uzrasas['text'] = f'Pajamos:\n\n{gauti_pajamas()}€'
    islaidu_uzrasas['text'] = f'Islaidos:\n\n-{gauti_islaidas()}€'

#   Istrina visus pasirinktus irasus
def istrinti_pasirinktus_irasus():
    pasirinkti_irasai = lentele.selection()
    for irasas in pasirinkti_irasai:
        lentele.delete(irasas)
        trinamas_irasas = session.query(Lentele).get(irasas)
        session.delete(trinamas_irasas)
        session.commit()
        atnaujinti_balansa_pajamas_islaidas()

        #   Prideda istrinta irasa i loggeri
        logging.info(f'Istrintas irasas\niraso id: ({trinamas_irasas.id}), '
                     f'iraso tipas: ({trinamas_irasas.tipas}), paskirtis: ({trinamas_irasas.paskirtis}), suma: ({trinamas_irasas.suma}),data: ({trinamas_irasas.iraso_data})')

#   Filtruoja irasus lenteleje pagal tipa ir raktazodi
def filtravimas():
    filtravimo_tipas = filtravimo_tipai.get()
    filtravimo_raktazodzis = filtravimo_raktazodzio_ivedimas.get().capitalize()

    if filtravimo_tipas == 'Visi':
        lentele.delete(*lentele.get_children())
        visi_irasai_lenteleje()

    if filtravimo_raktazodzis != '':
        lentele.delete(*lentele.get_children())

        if filtravimo_tipas == 'ID':
            filtruoti_irasai = session.query(Lentele).filter_by(id=filtravimo_raktazodzis).all()
            filtravimo_raktazodzio_ivedimas.delete(0, END)
            for irasas in filtruoti_irasai:
                lentele.insert(parent='', index='end', iid=irasas.id, text='', values=(irasas.id, irasas.tipas, irasas.paskirtis, irasas.suma, irasas.iraso_data))

        if filtravimo_tipas == 'Iraso tipas':
            filtruoti_irasai = session.query(Lentele).filter_by(tipas=filtravimo_raktazodzis).all()
            filtravimo_raktazodzio_ivedimas.delete(0, END)
            for irasas in filtruoti_irasai:
                lentele.insert(parent='', index='end', iid=irasas.id, text='', values=(irasas.id, irasas.tipas, irasas.paskirtis, irasas.suma, irasas.iraso_data))

        if filtravimo_tipas == 'Paskirtis':
            filtruoti_irasai = session.query(Lentele).filter_by(paskirtis=filtravimo_raktazodzis).all()
            filtravimo_raktazodzio_ivedimas.delete(0, END)
            for irasas in filtruoti_irasai:
                lentele.insert(parent='', index='end', iid=irasas.id, text='', values=(irasas.id, irasas.tipas, irasas.paskirtis, irasas.suma, irasas.iraso_data))

        if filtravimo_tipas == 'Suma':
            filtruoti_irasai = session.query(Lentele).filter_by(suma=filtravimo_raktazodzis).all()
            filtravimo_raktazodzio_ivedimas.delete(0,END)
            for irasas in filtruoti_irasai:
                lentele.insert(parent='', index='end', iid=irasas.id, text='', values=(irasas.id, irasas.tipas, irasas.paskirtis, irasas.suma, irasas.iraso_data))

        if filtravimo_tipas == 'Iraso data':
            filtruoti_irasai = session.query(Lentele).filter_by(iraso_data=filtravimo_raktazodzis).all()
            filtravimo_raktazodzio_ivedimas.delete(0,END)
            for irasas in filtruoti_irasai:
                lentele.insert(parent='', index='end', iid=irasas.id, text='', values=(irasas.id, irasas.tipas, irasas.paskirtis, irasas.suma, irasas.iraso_data))


#   Sukuriamas rysys su duomenu baze

engine = create_engine('sqlite:///biudzeto_duomenu_baze.db')
Session = sessionmaker(bind=engine)
session = Session()

#   Sukuriamas loggeris

logging.basicConfig(filename='biudzetas_logeris.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

pasirinkimai = ['Visi', 'ID', 'Iraso tipas', 'Paskirtis', 'Suma', 'Iraso data']

#   Langu sukurimas
programa = Tk()

programa.title('Biudzeto programa')
programa.iconbitmap(r'euro.ico')
programa.geometry('900x600')
kaire = Frame(programa, bd=1, relief=RAISED, bg='#8a8a87')
vidurys = Frame(programa, bd=1, relief=RAISED, bg='#8a8a87')
vidurys_virsus = Frame(vidurys, bg='#8a8a87')
vidurys_apacia = Frame(vidurys, bg='#8a8a87')
vidurys_apacia_kaire = Frame(vidurys_apacia, bg='#8a8a87')
vidurys_apacia_desine = Frame(vidurys_apacia, bg='#8a8a87')
desine = Frame(programa, bd=1, relief=RAISED, bg='#8a8a87')

#   Mygtyku, uzrasu ir lenteles aprasymas

#   Kaire puse
prideti_pajamas_mygtukas = Sukurti_mygtuka(kaire, 'Prideti irasa')
pakeisti_irasa_mygtukas = Sukurti_mygtuka(kaire, 'Pakeisti irasa')
istrinti_irasa_mygtukas = Button(kaire, text='Istrinti irasa/us', command=istrinti_pasirinktus_irasus, bg='#b3b3b1')

#   Vidurio virsutine puse
style_lentele = ttk.Style()
style_lentele.theme_use('alt')
style_lentele.configure('Treeview', background='#dededc', foreground='black', fieldbackground='#dededc')
style_lentele.map('Treeview', background=[('selected', '#9e9e9e')])


lenteles_scroll = Scrollbar(vidurys_virsus)
lentele = ttk.Treeview(vidurys_virsus,yscrollcommand=lenteles_scroll.set)
lenteles_scroll.config(command=lentele.yview)
lentele['columns'] = ('ID', 'Iraso tipas', 'Paskirtis', 'Suma', 'Iraso data')
lentele.column('#0', width=0, stretch=NO)
lentele.column('ID', anchor=W, width=10)
lentele.column('Iraso tipas', anchor=W, width=40)
lentele.column('Paskirtis', anchor=W, width=150)
lentele.column('Suma', anchor=W, width=50)
lentele.column('Iraso data', anchor=W, width=50)
lentele.heading('ID', text='ID', anchor=W)
lentele.heading('Iraso tipas', text='Iraso tipas', anchor=W)
lentele.heading('Paskirtis', text='Paskirtis', anchor=W)
lentele.heading('Suma', text='Suma', anchor=W)
lentele.heading('Iraso data', text='Iraso data', anchor=W)
visi_irasai_lenteleje()

#   Vidurio apacios kaire puse
filtravimo_tipo_uzrasas = Label(vidurys_apacia_kaire, text='Filtruoti pagal:', bg='#8a8a87')
filtravimo_raktazodzio_uzrasas = Label(vidurys_apacia_kaire, text='Raktazodis:', bg='#8a8a87')

#   Vidurio apacios desine puse
style_filtravimo_tipai = ttk.Style()
style_filtravimo_tipai.theme_use('alt')
style_filtravimo_tipai.configure('TCombobox', fieldbackground='#dededc', background='#dededc')
style_filtravimo_tipai.map('TCombobox', background=[('readonly', '#dededc')])

filtravimo_raktazodzio_ivedimas = Entry(vidurys_apacia_desine, bg='#dededc')
filtravimo_tipai = ttk.Combobox(vidurys_apacia_desine, values=pasirinkimai)
filtravimo_tipai.current(0)
filtravimo_mygtukas = Button(vidurys_apacia_desine, text='Filtruoti', width=16, bg='#b3b3b1', command=filtravimas)

#   Desine puse
balanso_uzrasas = Label(desine, text=f'Balansas:\n\n{gauti_balansa()}€', bg='#8a8a87')
pajamu_uzrasas = Label(desine, text=f'Pajamos:\n\n{gauti_pajamas()}€', bg='#8a8a87', fg='#80f725')
islaidu_uzrasas = Label(desine, text=f'Islaidos:\n\n-{gauti_islaidas()}€', bg='#8a8a87', fg='#fc4c3f')

#   Packinimas
#   Langai
kaire.pack(side=LEFT, fill=BOTH, expand=1)
vidurys.pack(side=LEFT, fill=BOTH, expand=1)
desine.pack(side=RIGHT, fill=BOTH, expand=1)
vidurys_virsus.pack(side=TOP, expand=1, fill=BOTH)
vidurys_apacia.pack(side=BOTTOM, expand=1, fill=BOTH)
vidurys_apacia_kaire.pack(side=LEFT, fill=BOTH, expand=1)
vidurys_apacia_desine.pack(side=RIGHT, fill=BOTH, expand=1)

#   Kaire puse
istrinti_irasa_mygtukas.pack(expand=1, anchor=N, side=TOP)

#   Vidurio virsus
lenteles_scroll.pack(side=RIGHT, fill=BOTH, pady=50)
lentele.pack(fill=BOTH, expand=1, pady=50)


#   Vidurio kaires apacia
filtravimo_tipo_uzrasas.pack(anchor=E)
filtravimo_raktazodzio_uzrasas.pack(anchor=E)

#   Vidurio desines apacia
filtravimo_tipai.pack(anchor=W)
filtravimo_raktazodzio_ivedimas.pack(anchor=W)
filtravimo_mygtukas.pack(anchor=W)

#   Desine puse
balanso_uzrasas.pack(expand=1)
pajamu_uzrasas.pack(expand=1)
islaidu_uzrasas.pack(expand=1)

programa.mainloop()
