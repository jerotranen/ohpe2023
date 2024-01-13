import calendar
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# tkinter -> https://docs.python.org/3/library/tkinter.html
# kalenteri -> https://docs.python.org/3/library/calendar.html
# datetime -> https://docs.python.org/3/library/datetime.html

root = tk.Tk()
root.title("Jeremiaksen kalenteri")
print("Muistutus esitettävä muodossa 'yymmdd-teksti'")

# Muistutus alustetaan tässä, jotta widget toimii
muistutus = tk.StringVar()

# Muistutusten ja kalenterin käsitteleminen
def lataa_kalenteri(year, month):
    muist_text = lataa_muistutus()
    muistutus_text.delete(1.0, tk.END)
    muistutus_text.insert(1.0, muist_text)
    cal_text = calendar.month(year, month)
    kalenteri_text.delete(1.0, tk.END)
    kalenteri_text.insert(1.0, cal_text)

    # Tästä eteenpäin merkataan muistutuksen päivämäärä kalenterinäkymään
    for tag in muist_text:
        tagyear = int(tag[:2]) + 2000
        tagmonth = int(tag[2:4])
        tagday = int(tag[4:6])

        if year == tagyear and month == tagmonth: # vuoden ja kuukauden tarkistus
            
            # Erotetun päivän etsiminen
            # Arvo 3.0 pakottaa haun alkamaan kolmannesta elementistä eli ensimmäisestä päivästä
            start_pos = kalenteri_text.search(str(tagday), "3.0", stopindex=tk.END)

            # Mikäli päivä löytyy, päivä merkataan tkinterin tagin avulla
            if start_pos:
                end_line, end_char = start_pos.split('.')
                end_pos = f"{end_line}.{int(end_char) + len(str(tagday))}" # tekstin osa joka merkataan
                kalenteri_text.tag_configure(tag, background="cyan") # määrittää merkkaamisen tyylin
                kalenteri_text.tag_add(tag, start_pos, end_pos) # lisää tyylin kyseiseen tekstiin


# Tässä luetaan tiedostosta muistutukset ja lisätään listaan, jota helppo käsitellä
def lataa_muistutus():
    muistutuslista = []
    try:
        with open("muistutukset.txt") as tiedosto:
            for line in tiedosto:
                muistutuslista.append(line.strip())
    except FileNotFoundError: # Jos tiedostoa ei löydy, tehdään sellainen
        with open("muistutukset.txt", "w"):
            pass
    return muistutuslista

# Muistutuksen lisääminen tiedostoon.
# Voidaan lisätä mitä tahansa tekstiä, mutta vain "yymmdd-teksti" formaatissa muistutukset toimivat oikein.
def kirjoita(muistutus):
    with open("muistutukset.txt", "a") as tiedosto:
        tiedosto.write(muistutus.get() + "\n")
    print("Muistutus lisätty")
    
# Tiedoston tyhjentäminen => muistutusten nollaaminen
def poista():
    with open("muistutukset.txt", "w") as tiedosto:
        tiedosto.write("")
    print("Muistutukset poistettu")
    
# Edellisen kuukauden lataaminen
def naytaedellinen():
    global year, month
    month -= 1
    if month == 0:
        month = 12
        year -= 1

    lataa_kalenteri(year, month)
    print("Näytetään", str(month) + "/" + str(year))

# Seuraavan kuukauden lataaminen
def naytaseuraava():
    global year, month
    month += 1
    if month == 13:
        month = 1
        year += 1

    lataa_kalenteri(year, month)
    print("Näytetään", str(month) + "/" + str(year))

# Widgeteissä ei voida kutsua useampaa funktiota, joten tämä on apufunktio, jotta useampaa saadaan kutsuttua
def kirjoita_ja_lataa():
    kirjoita(muistutus)
    lataa_kalenteri(year, month)

# Widgeteissä ei voida kutsua useampaa funktiota, joten tämä on apufunktio, jotta useampaa saadaan kutsuttua
def poista_ja_lataa():
    poista()
    lataa_kalenteri(year, month)

# Napit
muistutukset = ttk.Button(root, text="Aseta muistutus muodossa 'yymmdd-teksti'", command=lambda: kirjoita_ja_lataa())
muistutukset.grid(row=2, column=5, padx=5, pady=5)
muistutukset_entry = ttk.Entry(root, textvariable=muistutus)
muistutukset_entry.grid(row=3, column=5, padx=5, pady=5)

poisto = ttk.Button(root, text="Poista kaikki muistutukset", command=lambda: poista_ja_lataa())
poisto.grid(row=4, column=5, padx=5, pady=5)

edellinen = ttk.Button(root, text="<-", command=lambda: naytaedellinen())
edellinen.grid(row=2, column=1, padx=5, pady=5)

seuraava = ttk.Button(root, text="->", command=lambda: naytaseuraava())
seuraava.grid(row=2, column=2, padx=5, pady=5)

# kalenteri display
kalenteri_text = tk.Text(root, height=10, width=20, wrap=tk.WORD)
kalenteri_text.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

# muistutus display
muistutus_text = tk.Text(root, height=10, width=20, wrap=tk.WORD,)
muistutus_text.grid(row=1, column=5, columnspan=5, padx=5, pady=5)

# Tässä määritetään tämänhetkinen aika, jonka perusteella kalenteri näytetään
aikanyt = datetime.now()
year = aikanyt.year
month = aikanyt.month

# Muistutusten lataaminen, ensimmäisen kalenterisivujen lataaminen ja loop
lataa_kalenteri(year, month)
root.mainloop()