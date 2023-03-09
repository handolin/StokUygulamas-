from re import T
import sys
import datetime
from genericpath import exists
import json
import os
from pathlib import Path
import sqlite3





def CreateDB():

    conn = sqlite3.connect('stokveri.db')

    createtable = """Create Table IF NOT EXISTS Urunler(
    id INTEGER PRIMARY KEY,
    urun_adi NOT NULL,
    urun_birimi NOT NULL,
    stok INTEGER NOT NULL,
    stok_alarm_miktari INTEGER NOT NULL
    );"""
    conn.execute(createtable)

    createtable = """Create Table IF NOT EXISTS StokIslemleri(
    id INTEGER PRIMARY KEY,
    urun_id INTEGER NOT NULL,
    tarih  DATETIME NOT NULL,
    islem_turu TEXTNOT NULL,
    miktar INTEGER NOT NULL  
    );"""
    conn.execute(createtable)

    
    
    conn.close()


def run_query(query):
    """
    SQLite veritabanı dosyası ve sorgu alır ve sorguyu çalıştırır. Sonucu geri döndürür.
    """
    conn = sqlite3.connect('stokveri.db')  # veritabanı bağlantısını aç
    cur = conn.cursor()  # imleci veritabanı üzerinde hareket ettirmek için kullanacağız
    cur.execute(query)  # sorguyu çalıştır
    conn.commit()
    rows = cur.fetchall()  # tüm satırları al
    conn.close()  # bağlantıyı kapat
    return rows  # satırları geri döndür


os.system('color')
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[3m'
    UNDERLINE = '\033[4m'





def Menu():  
    yeniSatir()
    yapilmakİstenenİslem = input(f"{bcolors.HEADER}{bcolors.BOLD}Lütfen yapmak istediğiniz işlemi seçiniz:\n{bcolors.ENDC}" + "1.Ürün Ekle\n2.Stok Girişi\n3.Stok Çıkışı\n4.Stok Listesi\n5.Stok İşlem Kayıtlarını Göster\n99.Çıkış\n")
    
    if yapilmakİstenenİslem == "1":
        UrunEkle()
    if yapilmakİstenenİslem == "2":
        StokGiris()
    if yapilmakİstenenİslem == "3":
        StokCikis()
    if yapilmakİstenenİslem == "4":
        StokGoruntule()
    if yapilmakİstenenİslem == "5":
        StokIslemleriGoruntule()
    if yapilmakİstenenİslem == "99":
        os.system('cls')
        quit()





def UrunEkle():
    yeniSatir()
    UrunAdi = input("Lütfen ürün adını giriniz: ").title()
    UrunBirimi = input("Lütfen ürün birimini giriniz: ").lower()
    UrunStogu = 0
    StokAlarmMiktari = int(input("Lütfen stok uyarı verme miktarını belirtiniz: "))

    Urun_kayitet( UrunAdi,UrunBirimi,UrunStogu,StokAlarmMiktari)



#Ürün kontrol ediyor, mevcut değilse yeni kayıt yapıyor.
def Urun_kayitet(UrunAdi,UrunBirimi,UrunStogu,StokAlarmMiktari):

   
    sqlresult = run_query(f"Select * from Urunler where urun_adi= '{UrunAdi}'")
    if len(sqlresult)> 0:
        print(f"{bcolors.FAIL}Ürün zaten vardır.{bcolors.ENDC}")
        islem = int(input(
            f"{bcolors.HEADER}{bcolors.BOLD}Lütfen yapmak istediğiniz işlemi seçiniz:\n{bcolors.ENDC}" + "1.Ana Menü\n2.Ürün Ekle\n"))
        if islem == 1:
            Menu()
        if islem == 2:
            UrunEkle()
    
    run_query(
        f"INSERT INTO Urunler (urun_adi, urun_birimi,stok,stok_alarm_miktari) VALUES ('{UrunAdi}','{UrunBirimi}',{UrunStogu},{StokAlarmMiktari})")


    print(f"{bcolors.OKGREEN}Ürün eklenmiştir.{bcolors.ENDC}")
    islem = int(input(f"{bcolors.HEADER}{bcolors.BOLD}Lütfen işlem seçiniz:\n{bcolors.ENDC}" + "1.Ana Menü\n2.Ürün Ekle\n3.Stok Girişi\n"))
    if islem == 1:
        Menu()
    if islem == 2:
        UrunEkle()
    if islem == 3:
        StokGiris()

 
def StokGiris():
    yeniSatir()
    UrunAdi = input("Lütfen stok giriceğiniz ürünün adını yazınız:  ").title()
    sqlresult = run_query(f"Select id,urun_birimi from Urunler where urun_adi= '{UrunAdi}'")
    if len(sqlresult) == 0:
        print(f"{bcolors.HEADER}Ürün liste de mevcut değildir.{bcolors.ENDC}")
        islem = int(input(f"{bcolors.HEADER}{bcolors.BOLD}Lütfen işlem seçiniz:\n{bcolors.ENDC}" + "1.Ana Menü\n2.Ürün Ekle\n3.Stok Girişi\n"))
        if islem == 1:
            Menu()
        if islem == 2:
            UrunEkle()
        if islem == 3:
            StokGiris()

    UrunId = sqlresult[0][0]
    UrunStokMiktari = (input("Stok miktarını giriniz (" + sqlresult[0][1] + '): '))
    run_query(f"UPDATE Urunler SET stok= stok + {UrunStokMiktari}  where id='{UrunId}' ")
    run_query(f"INSERT INTO StokIslemleri (urun_id,tarih,islem_turu,miktar) values ({UrunId},'{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}','Giriş',{UrunStokMiktari})")
    print(f"{bcolors.OKGREEN}Ürün stok miktarı eklenmiştir.{bcolors.ENDC}")
    Menu()

    
    
    
def StokCikis():
    yeniSatir()
    UrunAdi = input("Lütfen stok çıkışı yapmak istediğiniz ürünün adını yazınız: ").title()
    sqlresult = run_query(f"Select id,urun_birimi from Urunler where urun_adi= '{UrunAdi}'")
    if len(sqlresult) == 0:
        print(f"{bcolors.HEADER}Ürün liste de mevcut değildir.{bcolors.ENDC}")
        islem = int(input(f"{bcolors.HEADER}{bcolors.BOLD}Lütfen işlem seçiniz:\n{bcolors.ENDC}" + "1.Ana Menü\n2.Ürün Ekle\n3.Stok Çıkışı\n"))
        if islem == 1:
            Menu()
        if islem == 2:
            UrunEkle()
        if islem == 3:
            StokCikis()
    
    UrunId = sqlresult[0][0]
    UrunStokMiktari =(input("Stok çıkış miktarını giriniz (" + sqlresult[0][1] + '): '))

    run_query(f"UPDATE Urunler SET stok = stok - {UrunStokMiktari}  where id='{sqlresult[0][0]}' ")
    sqlresult1 = run_query(f"Select id,stok from Urunler where urun_adi= '{UrunAdi}'")

    run_query(f"INSERT INTO StokIslemleri (urun_id,tarih,islem_turu,miktar) values ({UrunId},'{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}','Çıkış',{UrunStokMiktari})")
    print(f"{bcolors.OKGREEN}{UrunAdi} stoğu güncellenmiştir. Güncel stok miktarı : {sqlresult1[0][1]} {sqlresult[0][1]}{bcolors.ENDC}")

    yeniSatir()

    islem = int(input(f"{bcolors.HEADER}{bcolors.BOLD}Lütfen işlem seçiniz:\n{bcolors.ENDC}" + "1.Ana Menü\n2.Stok Çıkışı\n"))
    if islem == 1:
        Menu()
    if islem == 2:
        StokCikis()
    Menu()

def StokGoruntule():
    yeniSatir()
    islem = int(input(f"{bcolors.HEADER}{bcolors.BOLD}Lütfen işlem seçiniz:\n{bcolors.ENDC}" + "1.Ana Menü\n2.Tümünü Göster\n3.Seçilen Ürünü Göster\n"))
    if islem == 1:
        Menu()

    if islem == 2:
        yeniSatir()
        sqlresult = run_query("Select urun_adi,stok,urun_birimi From Urunler")
        print(sqlresult)
        Menu()
       
       
    if islem == 3:
        yeniSatir()
        UrunAdi = input("Lütfen stok miktarını görmek istediğiniz ürünün adını yazınız: ").title()
        sqlresult = run_query(f"Select id,stok,urun_birimi from Urunler where urun_adi= '{UrunAdi}'")
        if len(sqlresult) == 0:
            print(f"{bcolors.FAIL}Ürün liste de mevcut değildir.{bcolors.ENDC}")
            StokGoruntule()            
            
        else:
             print(f"{UrunAdi} : {sqlresult[0][1]} {sqlresult[0][2]}")
             Menu()









def StokIslemleriGoruntule():
    yeniSatir()
    sqlresult = run_query(f"Select * from StokIslemleri")
    if len(sqlresult) == 0:
        print(f"{bcolors.FAIL}Kayıt yoktur.{bcolors.ENDC}")
        Menu()  

    else:    
        islem = int(input(f"{bcolors.HEADER}{bcolors.BOLD}Lütfen işlem seçiniz:\n{bcolors.ENDC}" + "1.Ana Menü\n2.Tüm Listenin Kaydını Göster\n3.Seçilen Ürünün Kaydını Göster\n"))        
        if islem == 1:
                Menu()
                yeniSatir()

        else:
            yeniSatir()
            SartUrun = ""
            if islem == 2:
                pass
            if islem == 3:
                UrunAdi = input("Lütfen stok işlem kaydını görmek istediğiniz ürünün adını yazınız: ").title()
                SartUrun = f" where u.urun_adi = '{UrunAdi}' "

            sqlresult = run_query(f"Select s.id,s.urun_id,u.urun_adi,s.tarih,s.islem_turu,s.miktar from StokIslemleri s inner join Urunler u on u.id=s.urun_id" + SartUrun)  
            if len(sqlresult) == 0:
                print(f"{bcolors.FAIL}Kayıt yoktur.{bcolors.ENDC}")
                StokIslemleriGoruntule()
            else:
                for x in sqlresult:
                    if x[4] == 'Giriş':                        
                        print(f"{bcolors.OKGREEN} {str(x[0]).ljust(20,' ')} {str(x[1]).ljust(20,' ')} {str(x[2]).ljust(20,' ')} {str(x[3]).ljust(20,' ')} {str(x[4]).ljust(20,' ')} {str(x[5]).ljust(20,' ')}\n{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.FAIL} {str(x[0]).ljust(20,' ')} {str(x[1]).ljust(20,' ')} {str(x[2]).ljust(20,' ')} {str(x[3]).ljust(20,' ')} {str(x[4]).ljust(20,' ')} {str(x[5]).ljust(20,' ')}\n{bcolors.ENDC}")      
            Menu()

        # 223-252 arasına kısa şekilde yazdık.
        # if islem == 2:
        #         yeniSatir()
        #         print(f"{bcolors.HEADER}{bcolors.BOLD}{'Stok Id'.ljust(20,' ')}{'Ürün Id'.ljust(20,' ')}{'Ürün Adı'.ljust(20,' ')}{'Tarih/Saat'.ljust(20,' ')} {'İşlem Türü'.ljust(20,' ')} {'Miktar'.ljust(20,' ')}  \n{bcolors.ENDC}")
        #         sqlresult = run_query(f"Select s.id,s.urun_id,u.urun_adi,s.tarih,s.islem_turu,s.miktar from StokIslemleri s inner join Urunler u on u.id=s.urun_id")
        #         for x in sqlresult:
        #             if x[4] == 'Giriş':                        
        #                 print(f"{bcolors.OKGREEN} {str(x[0]).ljust(20,' ')} {str(x[1]).ljust(20,' ')} {str(x[2]).ljust(20,' ')} {str(x[3]).ljust(20,' ')} {str(x[4]).ljust(20,' ')} {str(x[5]).ljust(20,' ')}\n{bcolors.ENDC}")
        #             else:
        #                 print(f"{bcolors.FAIL} {str(x[0]).ljust(20,' ')} {str(x[1]).ljust(20,' ')} {str(x[2]).ljust(20,' ')} {str(x[3]).ljust(20,' ')} {str(x[4]).ljust(20,' ')} {str(x[5]).ljust(20,' ')}\n{bcolors.ENDC}")
 
        #         Menu()
        # if islem == 3:
        #         yeniSatir()
        #         UrunAdi = input("Lütfen stok işlem kaydını görmek istediğiniz ürünün adını yazınız: ").title()
        #         KayitVarmi = False
        #         print(f"{bcolors.HEADER}{bcolors.BOLD}{'Stok Id'.ljust(20,' ')}{'Ürün Id'.ljust(20,' ')}{'Ürün Adı'.ljust(20,' ')}{'Tarih/Saat'.ljust(20,' ')} {'İşlem Türü'.ljust(15,' ')} {'Miktar'.ljust(15,' ')}  \n{bcolors.ENDC}")
        #         sqlresult = run_query(f"Select s.id,s.urun_id,u.urun_adi,s.tarih,s.islem_turu,s.miktar from StokIslemleri s inner join Urunler u on u.id=s.urun_id where u.urun_adi = '{UrunAdi}'")
        #         for x in sqlresult:
        #             if x[4] == 'Giriş':                        
        #                 print(f"{bcolors.OKGREEN} {str(x[0]).ljust(20,' ')} {str(x[1]).ljust(20,' ')} {str(x[2]).ljust(20,' ')} {str(x[3]).ljust(20,' ')} {str(x[4]).ljust(20,' ')} {str(x[5]).ljust(20,' ')}\n{bcolors.ENDC}")
        #             else:
        #                 print(f"{bcolors.FAIL} {str(x[0]).ljust(20,' ')} {str(x[1]).ljust(20,' ')} {str(x[2]).ljust(20,' ')} {str(x[3]).ljust(20,' ')} {str(x[4]).ljust(20,' ')} {str(x[5]).ljust(20,' ')}\n{bcolors.ENDC}")
 
        #             KayitVarmi = True
                    
        #         if not KayitVarmi:
        #             print(f"{bcolors.FAIL}Ürün stok kaydı bulunamadı.{bcolors.ENDC}")
        #             StokIslemleriGoruntule()

        #         Menu()
                
   

def StokAnaSayfaUyari():
    

    sqlresult = run_query(f"Select urun_adi, stok,urun_birimi from Urunler where stok < stok_alarm_miktari")

    print(f"{bcolors.FAIL}{bcolors.BOLD} \n{'STOK UYARI'.center(40,'-')} \n{bcolors.ENDC}")
    for x in sqlresult:       
        print(x)


            





def yeniSatir():
    Satir = '-'.center(100,"-")
    print(Satir)


StokAnaSayfaUyari()  
CreateDB()

Menu()


