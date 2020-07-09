import matplotlib
import matplotlib.pyplot as plt
import requests
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")
plt.style.use("seaborn")

#-------------------------------------------------------------------------------------------------------
#                              FONKSİYONLARI TANIMLIYORUZ
#-------------------------------------------------------------------------------------------------------

#grafiklerimizi çizecek ve bunları kanvasa ardından da frame'e yerleştirecek fonksiyonu oluşturalım
def grafik_cizici(ulke):
    # her grafik çizişimizde önceki frame'i yok edeceğiz
    global frameGrafik
    frameGrafik.destroy()
    frameGrafik = tk.Frame(pencere)
    frameGrafik.pack(side=tk.LEFT)

    # apiden kodu okuyalım ve kaydedelim
    infoURL = "https://api.covid19api.com/total/dayone/country/" + ulke
    kaynakKod = requests.get(infoURL)
    kaynakListe = kaynakKod.json()

    # eyaletli ülkeler için başka bir link kullanmamız gerekiyor
    if kaynakListe == []:
        infoURL = "https://api.covid19api.com/total/country/" + ulke
        kaynakKod = requests.get(infoURL)
        kaynakListe = kaynakKod.json()

    # grafiklerdeki verileri saklayacağımız listeleri oluşturalım.
    x = []
    y = []
    yeniY = []
    olumY = []
    toplamOluY = []

    # tkinter ekranına ekleyeceğimiz bir kanvas ve onun içine oturacak figürü oluşturalım
    fig, axs = plt.subplots(2, 3, figsize=(30, 30))
    bar1 = FigureCanvasTkAgg(fig, master=frameGrafik)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    axs[1,2].set_visible(False)

    # günlük enfekte kişi sayısı grafiğini çizelim ve ekrana koyalım
    for i in range(1, len(kaynakListe)):
        vaka = kaynakListe[i]["Confirmed"] - kaynakListe[i - 1]["Confirmed"]
        y.append(vaka)
    for i in range(1, len(kaynakListe)):
        x.append(i)

    axs[0, 0].bar(x, y, label="enfekte olanlar")
    axs[0, 0].set_title("günlük enfekte olan grafiği")

    # ----------------------------------------------
    # günlük aktif vaka sayısı grafiğini çizelim ve ekrana koyalım
    for i in range(1, len(kaynakListe)):
        yeniY.append(kaynakListe[i]["Active"])

    axs[0, 1].plot(x, yeniY)
    axs[0, 1].set_title("toplam enfekte kişi sayısı grafiği")
    axs[0, 1].fill_between(x, yeniY, 0, alpha=0.3, facecolor="black")

    # ----------------------------------------------
    # günlük ölüm grafiğini çizelim
    for i in range(1, len(kaynakListe)):
        olum = kaynakListe[i]["Deaths"] - kaynakListe[i - 1]["Deaths"]
        olumY.append(olum)

    axs[1, 0].bar(x, olumY)
    axs[1, 0].set_title("günlük ölen sayısı grafiği")

    # ----------------------------------------------
    # toplam ölüm grafiğini çizelim ve ekrana koyalım
    for i in range(1, len(kaynakListe)):
        toplamOlum = kaynakListe[i]["Deaths"]
        toplamOluY.append(toplamOlum)

    axs[1, 1].plot(x, toplamOluY)
    axs[1, 1].set_title("toplam ölen sayısı grafiği")

    # ----------------------------------------------
    # dünkü iyileşen, dünkü enfekte olan ve dünkü ölüm sayısını pie grafik
    # şeklinde gösterelim
    dunkuVaka = kaynakListe[len(kaynakListe)-1]["Confirmed"] - kaynakListe[len(kaynakListe)-2]["Confirmed"]
    dunkuOlum = kaynakListe[len(kaynakListe)-1]["Deaths"] - kaynakListe[len(kaynakListe)-2]["Deaths"]
    dunkuIyilesen = kaynakListe[len(kaynakListe)-1]["Recovered"] - kaynakListe[len(kaynakListe)-2]["Recovered"]
    bolumler = [dunkuVaka,dunkuIyilesen,dunkuOlum]
    etiketler = ["vaka", "iyileşme","ölüm"]
    renkler = ["#008fd5","#fc4f30","#e5ae37"]
    axs[0,2].pie(bolumler, labels=etiketler,startangle=90,autopct="%1.1f%%", colors= renkler)
    axs[0,2].set_title("dünkü veriler")
    # -----------------------------------------------


def dunyaVerileri():

    en_cok_olum = []
    en_cok_olumX = []
    en_cok_vaka = []
    en_cok_vakaX = []
    dictVaka = {}

    global frameGrafik
    frameGrafik.destroy()
    frameGrafik = tk.Frame(pencere)
    frameGrafik.pack(side=tk.LEFT)

    fig, axs = plt.subplots(2, figsize=(10, 10))
    canvas = FigureCanvasTkAgg(fig, master=frameGrafik)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    # url = "https://api.covid19api.com/summary"
    # URL = requests.get(url).json()
    # yeniURL = URL["Countries"]

    url = "https://coronavirus-19-api.herokuapp.com/countries"
    URL = requests.get(url).json()
    for i in range(1, len(ulkeIsimleri)):
        try:
            dictVaka[URL[i]["country"]] = URL[i]["cases"] - URL[i]["recovered"]
        except:
            pass
    duzenliDict = sorted(dictVaka.items(),key=lambda x: x[1], reverse=True)

    # şimdi en çok vaka olan ülkeleri bulduk ve bunlarla bir sözlük oluşturduk sıra bunları grafiğe dönüştürmekte
    # bunun için sözlükteki key-value pairlerini iki ayrı listeye for döngüsüyle dönüştüreceğim
    for i in range(len(duzenliDict)-195):
        en_cok_vaka.append(duzenliDict[i][1])
        en_cok_vakaX.append(duzenliDict[i][0])
    axs[0].barh(en_cok_vakaX, en_cok_vaka, label="en çok vaka sayısı olan ülkeler")
    axs[0].set_title("aktif vaka sayısı en çok olan ülkeler")

    # en çok ölüm gerçekleşen ülkelerin grafiğini oluşturalım yukarıdaki mantık çerçevesinde
    for i in range(1, len(ulkeIsimleri)):
        try:
            dictVaka[URL[i]["country"]] = URL[i]["deaths"]
        except:
            pass
    duzenliDict = sorted(dictVaka.items(),key=lambda x: x[1], reverse=True)

    for i in range(len(duzenliDict)-195):
        en_cok_olum.append(duzenliDict[i][1])
        en_cok_olumX.append(duzenliDict[i][0])
    axs[1].barh(en_cok_olumX, en_cok_olum, label="en çok ölüm olan ülkeler")
    axs[1].set_title("en çok ölüm olan ülkeler")


    sonURL = "https://api.covid19api.com/world/total"
    sonURL = requests.get(sonURL).json()

    yazi1 = tk.Label(frameGrafik, text="Dünya Toplam İstatistikler", font=("Helvetica", 12))
    yazi1.pack(side=tk.TOP)

    yazi2 = tk.Label(frameGrafik, text="toplam vaka: " + str(sonURL["TotalConfirmed"]), font=("Liberation-Serif", 10))
    yazi2.pack(side=tk.TOP)

    yazi3 = tk.Label(frameGrafik, text="toplam ölüm: " + str(sonURL["TotalDeaths"]), font=("Liberation-Serif", 10))
    yazi3.pack(side=tk.TOP)

    yazi4 = tk.Label(frameGrafik, text="toplam iyileşme: " + str(sonURL["TotalRecovered"]), font=("Liberation-Serif", 10))
    yazi4.pack(side=tk.TOP)


def butonCizme():
    for i in range(len(ulkeIsim)):
        if ulkeIsim[i]["Country"] == ulkeList.selection_get():
            grafik_cizici(ulkeIsim[i]["Slug"])


# ülke aratma fonksiyonunu yazalım
def arat():
    aranan = aramaEntry.get()
    for i in range(0, ulkeList.size()):
        if aranan == ulkeList.get(i):
            grafik_cizici(aranan)


# kullanıcı programı kapatmak isterse soru soralım
def kapamaIstek():
    sonuc = messagebox.askyesno("Uyarı",message="Kapatmak istediğinize emin misiniz?")
    if sonuc:
        exit()

def kapama():
    exit()

def anaSayfa():
    kilavuzPen.destroy()
# ----------------------------------------------------------------------------------------------------------------------
#                              kullanım kılavuzu penceresini oluşturalım
# ----------------------------------------------------------------------------------------------------------------------

kilavuzPen = tk.Tk()
kilavuzPen.title("kullanım kılavuzu")
kilavuzPen.geometry("500x400")


kilavuzBaslik = tk.Label(kilavuzPen, text="DİKKAT!\n", font=("Helvetica", 16))
kilavuzBaslik.pack()

kilavuzText1 = tk.Label(kilavuzPen, text="yazan: \n Ahmet Fehim Örnek \n 1191602071 \n Bilgisayar Mühendisliği\n \n ", font=("Verdana", 10))
kilavuzText1.pack()

kilavuzText2 = tk.Label(kilavuzPen, text="arayacağınız ülkeyi bulmak zor geliyorsa ismini ingilizce slug \n şekilde yazıp arat ve çiz butonuna basınız\n", font=("Verdana", 10))
kilavuzText2.pack()

kilavuzText3 = tk.Label(kilavuzPen, text="uygulamanın çalışabilmesi için requests modülü kurulu olmalıdır\n", font=("Verdana", 10))
kilavuzText3.pack()

kilavuzText4 = tk.Label(kilavuzPen, text="kullanım kolaylığını esas aldığımdan olabildiğince minimal\n bir arayüz tasarlamaya çalıştım \n \n ", font=("Verdana", 10))
kilavuzText4.pack()

kilavuzText5 = tk.Label(kilavuzPen, text="devam etmek istiyorsanız butona basabilirsiniz", font=("Verdana", 8))
kilavuzText5.pack()

anladimBut = ttk.Button(kilavuzPen, text="Anladım", command=anaSayfa)
anladimBut.pack()

kilavuzPen.protocol("WM_DELETE_WINDOW", kapama)
kilavuzPen.mainloop()
# ------------------------------------------------------------------------------------------------------------------------------------
#                                                 ana pencereyi oluşturalım
# ------------------------------------------------------------------------------------------------------------------------------------
pencere = tk.Tk()
pencere.title("COVID-19 Grafikleri")
pencere.geometry("1400x700")

solFrame = tk.Frame(pencere)
ustFrame = tk.Frame(pencere)
frameGrafik = tk.Frame(pencere)


dunyaVeriButonu = ttk.Button(ustFrame, text="          Dünya İstatistikleri           ", command=dunyaVerileri)
dunyaVeriButonu.pack(side=tk.TOP)
aramaEntry = tk.Entry(ustFrame, width=15)
aramaEntry.pack(side = tk.LEFT)
aramaButon = ttk.Button(ustFrame, command= arat, text="arat ve çizdir")
aramaButon.pack(side = tk.LEFT)
cizme = ttk.Button(solFrame, text="     Grafikleri Çiz     ", command= butonCizme)
cizme.pack(side=tk.TOP)
ulkeList = tk.Listbox(solFrame)
ulkeList.pack(side= tk.LEFT, fill=tk.Y)
ulkeScroll = tk.Scrollbar(solFrame, orient= tk.VERTICAL)
ulkeScroll.pack(side=tk.LEFT, fill=tk.BOTH)
ulkeList.config(yscrollcommand= ulkeScroll.set)
ulkeScroll.config(command= ulkeList.yview)

ustFrame.pack(side=tk.TOP, anchor=tk.NW)
solFrame.pack(side=tk.LEFT, fill=tk.Y)
frameGrafik.pack(side=tk.LEFT)

ulkeIsim = requests.get("https://api.covid19api.com/countries").json()
ulkeIsimleri = []

# ülkeleri alfebetik olarak ulkeList listbox'ına ekleyelim
for i in range(len(ulkeIsim)):
    ulkeIsimleri.append(ulkeIsim[i]["Country"])

duzenleIsim = sorted(ulkeIsimleri)
for i in range(len(ulkeIsim)):
    ulkeList.insert(tk.END, duzenleIsim[i])

pencere.protocol("WM_DELETE_WINDOW",kapamaIstek)
pencere.mainloop()
