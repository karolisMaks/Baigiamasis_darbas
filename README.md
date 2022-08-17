# Biudzeto programa

### Veikimo principas:

- Pirmą kartą paleidus main.py programą, automatiškai susikuria duomenų bazė, loginimo file'as ir
įsijungia su tkinter moduliu padaryta grafinė sąsaja.

- Programa visus įrašus ir jų pakitimus saugo duomenu bazės fail'e - biudzeto_duomenu_baze.db
Taip pat visi įrašai ir jų pakitimai yra logginami į - biudzetas_logeris.log fail'ą

- Pagrindiniame lange rodoma viso biudžeto balansas, pajamos ir išlaidos, kurios keičiasi
gyvu laiku įvedus naują įrašą, ištrynus įrašą arba pakeitus esamo įrašo sumą

### Programoje galima: 
- Pridėti naujus įrašus nurodant jų tipą, paskirtį, sumą ir datą
- Pakeisti esamų irašų tipą, paskirtį, sumą ir datą
- Ištrinti esamus įrašus
- Filtruoti lentelėje rodomus įrašus pagal norimą raktažodį
- Matyti biudžeto balansą, bendrą pajamų sumą ir bendrą išlaidų sumą

### Pastabos:
- Įvedant naują įrašą arba keičiant esamą, data privaloma vesti XXXX-XX-XX formatu
