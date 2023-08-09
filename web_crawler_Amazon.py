from implementing_filters import WebCrawler
from requests import get
from requests.exceptions import ConnectionError
from tkinter import messagebox
from tkinter import *
from excel_exporter import *


# before starting the program check internet status
try:
    check = get("https://www.google.com")

except ConnectionError:
    messagebox.showerror("HATA", "İNTERNET BAZLI BİR HATA MEYDANA GELDİ\n\n\n"
                                 "İNTERNET BAĞLANTISINI KONTROL EDİNİZ...")

    exit()

# starting gui

window = Tk()

# set options of crawler class

craw = WebCrawler()

# window confs

window.title("Amazoncu")

window.geometry("800x400+430+180")

# main label and other labels

main_label = Label(window, text="AMAZON.COM", font=("Rosewood Std Regular", 25), fg="dark green")

main_label.grid(row=0, column=2, ipady=3, pady=20)

# search label

search_label = Label(window, text="ARANACAK KELİME :", font=("Italic", 13), fg="brown4")

search_label.grid(row=1, column=1, pady=30, padx=25)

# max min price

max_min_label = Label(window, text="MAX & MİN FİYAT :", font=("Italic", 13), fg="brown4")

max_min_label.place(x=25, y=180)

# star label

star_label = Label(window, text="YILDIZ ÜSTÜ OLSUN :", font=("Italic", 13), fg="brown4")

star_label.grid(row=4, column=1, padx=25)

# page num label

page_num = Label(window, text="KAÇ SAYFA VERİ :", font=("Italic", 13), fg="brown4")

page_num.grid(row=5, column=1, padx=25)

# product label

product_label = Label(window, font="Times 12 bold", text="KAZINAN ÜRÜN : ŞU ANLIK YOK\n"
                                                         "HAYDİ KAZIYALIM ")

product_label.grid(row=0, column=1)

# sponsor checkbox

variable_for_checkbox = IntVar()

sponsor_checkbox = Checkbutton(window, text="Sponsorlu ürünleri göster", variable=variable_for_checkbox,
                               font=("Italic", 13))

sponsor_checkbox.grid(row=3, column=2, pady=40)

# max and min price

max_entry = Entry(textvariable=StringVar(value="$ Max "), width=15)

max_entry.place(x=160, y=220)

min_entry = Entry(textvariable=StringVar(value="$ Min "), width=15)

min_entry.place(x=30, y=220)

# star main_inf

spinbox = Spinbox(window, from_=1, to=4, textvariable=StringVar(value="0"), wrap=True, width=50)

spinbox.grid(row=4, column=2, pady=10, ipady=2, padx=25)

# entry

search_entry = Entry(width=50)

search_entry.grid(row=1, column=2, padx=25, ipady=2)

# page num spinbox

spinbox_pagenum = Spinbox(window, from_=1, to=200, textvariable=StringVar(value="0"), wrap=True, width=50)

spinbox_pagenum.grid(row=5, column=2, pady=10, ipady=2, padx=25)

# menubar function

# function off button

def scrap():

    # changing default vars

    # get info from gui

    product_numbers = 0

    row_number = 0

    row_number2 = 0

    craw.details_dictionary = []

    craw.keyword = search_entry.get().replace(" ", "+")

    craw.min_price = min_entry.get()

    craw.max_price = max_entry.get()

    craw.stars = int(spinbox.get())

    craw.sponsor_support = variable_for_checkbox.get()

    craw.until_page_num = int(spinbox_pagenum.get())

    # first of all extract main information

    for page_number in range(1, craw.until_page_num + 1):
        # crawl amazon

        craw.details_of_products(craw.request_the_page_and_parse(page_number))

    # as a second operation get detailsed info from links

    for link in craw.details_dictionary:
        craw.link_details_products(link["Ürün linki"])

        product_numbers += 1

        # update the window to change label configs

        product_label.config(text=f"Bulunan Ürün : {len(craw.details_dictionary)}\n\n"
                                  f"Kazınan Ürün : {product_numbers}/{len(craw.details_dictionary)}")

        window.update()

        # information to import excel file

    for main_inf in craw.details_dictionary:
        row_number += 1

        import_excel_file_main(row_number, main_inf["ürün adı"], float(main_inf["ürün fiyatı"]), main_inf["Yıldız"],
                               main_inf["Ürün linki"])

    # secondary information

    for details in craw.details_dictionary2:
        row_number2 += 1

        import_excel_file_detail(row_number2, details["Görüntülünme"], details["Shipping ücreti"],
                                 details["Stock drumu"], details["Gönderen"], details["Tarafından Satılır"])

# the button to scrap

scrap_button = Button(window, text="Kazımaya başla", bg="black", fg="snow", height=7, command=scrap, borderwidth=8)

scrap_button.place(x=600, y=150)

window.mainloop()

