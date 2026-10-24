from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time
import sqlite3
import xml.etree.ElementTree as ET

con = sqlite3.connect("vbAltyapi.db")
cursor = con.cursor()
class altyapi:

        def __init__(self):
            self.browserProfile = webdriver.ChromeOptions()
            self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
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
            self.siralama.clear()
            kategori = Select(self.browser.find_element(By.ID, "icerik_ddlSkategori"))
            kategori.select_by_value(yas)
            time.sleep(8)
            kume = Select(self.browser.find_element(By.ID, "icerik_ddlskume"))
            kume.select_by_value(lig)
            time.sleep(8)
            yarisma = Select(self.browser.find_element(By.ID, "icerik_ddlSyarismaadi"))
            yarisma.select_by_value(liggrup)
            time.sleep(15)
            takimlar = self.browser.find_element(By.ID,"icerik_GvTemplate_1").find_elements(By.TAG_NAME,"tr")
            print(takimlar)
            for takim in takimlar:
                if takim.find_element(By.TAG_NAME,"a"):
                    takim = takim.find_element(By.TAG_NAME,"a").text
                self.siralama.append(takim)
            for a in range(len(takimlar)-1):
                    k = "icerik_GvTemplate_1_gO_"+ str(a)
                    oynanan = self.browser.find_element(By.ID,k).text
                    self.siralama.append(oynanan)
            for a in range(len(takimlar)-1):
                    k = "icerik_GvTemplate_1_gG_"+ str(a)
                    galibiyet = self.browser.find_element(By.ID,k).text
                    self.siralama.append(galibiyet)
            for a in range(len(takimlar) - 1):
                    k = "icerik_GvTemplate_1_gM_" + str(a)
                    maglubiyet = self.browser.find_element(By.ID,k).text
                    self.siralama.append(maglubiyet)
            for a in range(len(takimlar)-1):
                    k = "icerik_GvTemplate_1_gP_"+ str(a)
                    puan = self.browser.find_element(By.ID,k).text
                    self.siralama.append(puan)
            for a in range(len(takimlar)-1):
                    k = "icerik_GvTemplate_1_gA_"+ str(a)
                    alinanSet = self.browser.find_element(By.ID,k).text
                    self.siralama.append(alinanSet)
            for a in range(len(takimlar) - 1):
                    k = "icerik_GvTemplate_1_gV_" + str(a)
                    verilenSet = self.browser.find_element(By.ID,k).text
                    self.siralama.append(verilenSet)
            for a in range(len(takimlar)-1):
                    k = "icerik_GvTemplate_1_gSAV_"+ str(a)
                    SAV = self.browser.find_element(By.ID,k).text
                    self.siralama.append(SAV)
            for a in range(len(takimlar)-1):
                    k = "icerik_GvTemplate_1_gSPAV_"+ str(a)
                    SPAV = self.browser.find_element(By.ID,k).text
                    self.siralama.append(SPAV)
            for a in range(len(takimlar) - 1):
                cursor.execute(
                "INSERT INTO puandurumu (grup, sira, takim, oynanan, galibiyet, maglubiyet, puan, alinanset, verilenset, sav, spav) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (grubu, str(a + 1), self.siralama[a + 1], self.siralama[a+1+((len(takimlar)-1)*1)], self.siralama[a+1+((len(takimlar)-1)*2)], self.siralama[a+1+((len(takimlar)-1)*3)], self.siralama[a+1+((len(takimlar)-1)*4)], self.siralama[a+1+((len(takimlar)-1)*5)], self.siralama[a+1+((len(takimlar)-1)*6)],self.siralama[a+1+((len(takimlar)-1)*7)],self.siralama[a+1+((len(takimlar)-1)*8)]))
                con.commit()

        def lig1(self):
            self.siralama.clear()
            self.browser.get(
                "https://fikstur.tvf.org.tr/PTW/MjAyNi0yMDI3/Sw%3d%3d/MUxL/QXJhYmljYSBDb2ZmZWUgSG91c2UgS2FkxLFubGFyIFZvbGV5Ym9sIDEuTGlnaQ%3d%3d")
            time.sleep(6)
            takimlar = self.browser.find_element(By.ID,"icerik_PuanTablosu_pnlgvlist1").find_elements(By.TAG_NAME, "tr")

            grubu = "1.Lig"
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gtakimadi_" + str(a)
                takim = self.browser.find_element(By.ID,k).text
                self.siralama.append(takim)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gO_" + str(a)
                oynanan = self.browser.find_element(By.ID,k).text
                self.siralama.append(oynanan)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gG_" + str(a)
                galibiyet = self.browser.find_element(By.ID,k).text
                self.siralama.append(galibiyet)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gM_" + str(a)
                maglubiyet = self.browser.find_element(By.ID,k).text
                self.siralama.append(maglubiyet)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gP_" + str(a)
                puan = self.browser.find_element(By.ID,k).text
                self.siralama.append(puan)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gA_" + str(a)
                alinanSet = self.browser.find_element(By.ID,k).text
                self.siralama.append(alinanSet)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gV_" + str(a)
                verilenSet = self.browser.find_element(By.ID,k).text
                self.siralama.append(verilenSet)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gSAV_" + str(a)
                SAV = self.browser.find_element(By.ID,k).text
                self.siralama.append(SAV)
            for a in range(len(takimlar) - 1):
                k = "icerik_PuanTablosu_gvliste3S_gSPAV_" + str(a)
                SPAV = self.browser.find_element(By.ID,k).text
                self.siralama.append(SPAV)

            for a in range(len(takimlar) - 1):
                cursor.execute(
                    "INSERT INTO puandurumu (grup, sira, takim, oynanan, galibiyet, maglubiyet, puan, alinanset, verilenset, sav, spav) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (grubu, str(a + 1), self.siralama[a], self.siralama[a + ((len(takimlar) - 1) * 1)],
                     self.siralama[a + ((len(takimlar) - 1) * 2)], self.siralama[a + ((len(takimlar) - 1) * 3)],
                     self.siralama[a + ((len(takimlar) - 1) * 4)], self.siralama[a + ((len(takimlar) - 1) * 5)],
                     self.siralama[a + ((len(takimlar) - 1) * 6)], self.siralama[a + ((len(takimlar) - 1) * 7)],
                     self.siralama[a + ((len(takimlar) - 1) * 8)]))
                con.commit()


def tabloolustur():
    cursor.execute("DROP TABLE IF EXISTS puandurumu")
    cursor.execute(
                "CREATE TABLE IF NOT EXISTS puandurumu (grup TEXT, sira TEXT, takim TEXT, oynanan TEXT, galibiyet TEXT, maglubiyet TEXT, puan TEXT, alinanset TEXT, verilenset TEXT, sav TEXT, spav TEXT)")
    con.commit()

def xmlyaz():
    cursor.execute("SELECT *FROM puandurumu")
    con.commit()
    result = cursor.fetchall()
    root = ET.Element('root')
    for a in range(len(result)):
                PuanDurumu = ET.SubElement(root, 'PuanDurumu')
                YasGrubu = ET.SubElement(PuanDurumu, 'Grup')
                Sira = ET.SubElement(PuanDurumu, 'Sira')
                Takim = ET.SubElement(PuanDurumu, 'Takim')
                Oynanan = ET.SubElement(PuanDurumu, 'Oynanan')
                Galibiyet = ET.SubElement(PuanDurumu, 'Galibiyet')
                Maglubiyet = ET.SubElement(PuanDurumu, 'Maglubiyet')
                Puan = ET.SubElement(PuanDurumu, 'Puan')
                AlinanSet = ET.SubElement(PuanDurumu, 'AlinanSet')
                VerilenSet = ET.SubElement(PuanDurumu, 'VerilenSet')
                SAV = ET.SubElement(PuanDurumu, 'SAV')
                SPAV = ET.SubElement(PuanDurumu, 'SPAV')
                YasGrubu.text = result[a][0]
                Sira.text = result[a][1]
                Takim.text = result[a][2]
                Oynanan.text = result[a][3]
                Galibiyet.text = result[a][4]
                Maglubiyet.text = result[a][5]
                Puan.text = result[a][6]
                AlinanSet.text = result[a][7]
                VerilenSet.text = result[a][8]
                SAV.text = result[a][9]
                SPAV.text = result[a][10]
                tree = ET.ElementTree(root)

                tree.write('/puandurumu.xml')

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
xmlyaz()
con.close()
app.browser.quit()
