from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.select import Select
import sqlite3
import xml.etree.ElementTree as ET
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import os

# Repo kök klasörü (scripts/ klasörünün bir üstü). DB ve XML yolları buna göre.
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML_KLASOR = os.path.join(KOK, "xml")
os.makedirs(XML_KLASOR, exist_ok=True)

con = sqlite3.connect(os.path.join(KOK, "vbAltyapi.db"))
cursor = con.cursor()
class altyapi:

        def __init__(self):
            self.browserProfile = webdriver.ChromeOptions()
            self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            # GitHub Actions'ta ekransız (headless) çalış; kendi bilgisayarında pencere açılmaya devam eder
            if os.environ.get("CI"):
                self.browserProfile.add_argument("--headless=new")
                self.browserProfile.add_argument("--no-sandbox")
                self.browserProfile.add_argument("--disable-dev-shm-usage")
                self.browserProfile.add_argument("--window-size=1920,1080")
            service = Service()
            self.browser = webdriver.Chrome(service=service, options=self.browserProfile)
            self.siralama = []

        def giris(self):
            self.browser.get("https://istanbul.voleyboliltemsilciligi.com/PuanDurumu")
            time.sleep(8)
            cinsiyet = Select(self.browser.find_element(By.ID, "icerik_ddlsbe"))
            cinsiyet.select_by_value('B')
            time.sleep(8)
        def secim( self, yas, lig, liggrup, takimadi, grubu):
            kategori = Select(self.browser.find_element(By.ID,"icerik_ddlSkategori"))
            kategori.select_by_value(yas)
            time.sleep(8)
            kume = Select(self.browser.find_element(By.ID,"icerik_ddlskume"))
            kume.select_by_value(lig)
            time.sleep(8)
            yarisma = Select(self.browser.find_element(By.ID,"icerik_ddlSyarismaadi"))
            yarisma.select_by_value(liggrup)
            time.sleep(8)

            for j in range(0,36):
                k = "icerik_gvmusabakaliste_gevsahibi_" + str(j)
                k2 = "icerik_gvmusabakaliste_gmisafir_" + str(j)
                try:
                    tk = self.browser.find_element(By.ID,k).text
                    tk2 = self.browser.find_element(By.ID,k2).text
                except:
                    tk="hata"
                    tk2="hata"
                if tk == takimadi or tk2 == takimadi:
                    taka = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gevsahibi_" + str(j)).text
                    takb = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gmisafir_" + str(j)).text
                    ska = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gseta_" + str(j)).text
                    skb = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gsetb_" + str(j)).text
                    sets = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gsetsonuclari_" + str(j)).text
                    sal = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gyer_" + str(j)).text
                    st = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gsaat_" + str(j)).text
                    tar = self.browser.find_element(By.ID,"icerik_gvmusabakaliste_gtarih_" + str(j)).text
                    cursor.execute("SELECT COUNT(grup) FROM fikstur WHERE takima = ? AND takimb = ? AND grup = ?", (taka, takb, grubu))
                    result = cursor.fetchone()
                    row_count = result[0]
                    if row_count == 0:
                        cursor.execute(
                            "INSERT INTO fikstur (grup, tarih, saat, salon, takima, takimb, skora, skorb, setler) VALUES (?,?,?,?,?,?,?,?,?)",
                            (grubu, tar, st, sal, taka, takb, ska, skb, sets))
                    else:
                        cursor.execute(
                            "UPDATE fikstur SET tarih = ?, saat = ?, salon = ?, skora = ?, skorb = ?, setler = ? WHERE takima = ? AND takimb = ? AND grup = ?",
                            (tar, st, sal, ska, skb, sets, taka, takb, grubu))
                    con.commit()

        def lig1(self):
            self.browser.get("https://fikstur.tvf.org.tr/FSW/MjAyNi0yMDI3/Sw%3d%3d/MUxL/QXJhYmljYSBDb2ZmZWUgSG91c2UgS2FkxLFubGFyIFZvbGV5Ym9sIDEuTGlnaQ%3d%3d")
            time.sleep(8)
            grubu = "1.Lig"

            for j in range(0,153):
                k = "icerik_FiksturSonuclu_gvmusabakaliste_gevsahibi_" + str(j)
                k2 = "icerik_FiksturSonuclu_gvmusabakaliste_gmisafir_" + str(j)
                try:
                    tk = self.browser.find_element(By.ID,k).text
                    tk2 = self.browser.find_element(By.ID,k2).text
                except:
                    tk="hata"
                    tk2="hata"
                if tk == "VAKIFBANK" or tk2 == "VAKIFBANK":
                    taka = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gevsahibi_" + str(j)).text
                    takb = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gmisafir_" + str(j)).text
                    ska = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gseta_" + str(j)).text
                    skb = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gsetb_" + str(j)).text
                    sets = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gsetsonuclari_" + str(j)).text
                    sal = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gyer_" + str(j)).text
                    st = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gsaat_" + str(j)).text
                    tar = self.browser.find_element(By.ID,"icerik_FiksturSonuclu_gvmusabakaliste_gtarih_" + str(j)).text
                    cursor.execute("SELECT COUNT(grup) FROM fikstur WHERE takima = ? AND takimb = ? AND grup = ?", (taka, takb, grubu))
                    result = cursor.fetchone()
                    row_count = result[0]
                    if row_count == 0:
                        cursor.execute(
                            "INSERT INTO fikstur (grup, tarih, saat, salon, takima, takimb, skora, skorb, setler) VALUES (?,?,?,?,?,?,?,?,?)",
                            (grubu, tar, st, sal, taka, takb, ska, skb, sets))
                    else:
                        cursor.execute(
                            "UPDATE fikstur SET tarih = ?, saat = ?, salon = ?, skora = ?, skorb = ?, setler = ? WHERE takima = ? AND takimb = ? AND grup = ?",
                            (tar, st, sal, ska, skb, sets, taka, takb, grubu))
                    con.commit()


def tabloolustur():
    cursor.execute("DROP TABLE IF EXISTS fikstur")
    cursor.execute("CREATE TABLE IF NOT EXISTS fikstur (grup TEXT, tarih TEXT, saat TEXT, salon TEXT, takima TEXT, takimb TEXT, skora TEXT, skorb TEXT, setler TEXT)")
    con.commit()

def xmlOlustur():
    cursor.execute("SELECT *FROM fikstur")
    con.commit()
    result = cursor.fetchall()
    root = ET.Element('root')
    for a in range(len(result)):   # eskiden "- 1" vardı, son maç XML'e yazılmıyordu
        Mac = ET.SubElement(root, 'Mac')
        Grup = ET.SubElement(Mac, 'Grup')
        Tarih = ET.SubElement(Mac, 'Tarih')
        Saat = ET.SubElement(Mac, 'Saat')
        Salon = ET.SubElement(Mac, 'Salon')
        TakimA = ET.SubElement(Mac, 'TakimA')
        TakimB = ET.SubElement(Mac, 'TakimB')
        SkorA = ET.SubElement(Mac, 'SkorA')
        SkorB = ET.SubElement(Mac, 'SkorB')
        Setler = ET.SubElement(Mac, 'Setler')

        Grup.text = result[a][0]
        Tarih.text = result[a][1]
        Saat.text = result[a][2]
        Salon.text = result[a][3]
        TakimA.text = result[a][4]
        TakimB.text = result[a][5]
        SkorA.text = result[a][6]
        SkorB.text = result[a][7]
        Setler.text = result[a][8]
    # Dosya döngünün dışında, bir kez ve UTF-8 olarak yazılır.
    # Dosya adında Türkçe karakter yok (fikstür -> fikstur): adres olarak kullanmak kolay olsun diye.
    tree = ET.ElementTree(root)
    tree.write(os.path.join(XML_KLASOR, 'fikstur.xml'), encoding='utf-8', xml_declaration=True)


tabloolustur()
app = altyapi()
app.lig1()
app.giris()
app.secim("GK", "GKSL", "20634*579ADA67-15DE-4114-9C5D-F168620212C6", "Vakıfbank", "Genç")
app.secim("KK", "KKSL", "20638*AD31DB1A-5975-4377-BA5C-8CCF69B5055C", "Vakıfbank", "Küçük")
app.secim("YK", "YKSL", "20637*6CF95B79-E251-4F24-A1F8-804B434FFBE3", "Vakıfbank A", "Yıldız A")
app.secim("YK", "YKSL", "20636*3E78AFA3-530A-40CC-860C-DF883C7419B3", "Vakıfbank B", "Yıldız B")
app.secim("MdK", "MDKSL", "20641*FBF43E38-2E6D-48A8-B56B-EB287A4BE704", "Vakıfbank", "Midi")

#final etabı
#app.secim("GK", "GKSL", "5615*3D7C167B-5EC3-4891-B942-06D514858310", "Vakıfbank", "Genç Final")
#app.secim("KK", "KKSL", "18749*D07133D0-C04B-43E2-85B4-F8B093B4D368", "Vakıfbank", "Küçük Final")
#app.secim("YK", "YKSL", "18891*4F516DCA-8704-40E9-A814-DD65B4EAD841", "Vakıfbank", "Yıldız Final")
#app.secim("MdK", "MDKSL", "18804*6232ACE3-AA71-450B-BBAF-54FF9AD9916F", "Vakıfbank", "Midi Final")

xmlOlustur()
con.close()
app.browser.quit()