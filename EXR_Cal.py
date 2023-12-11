from tkinter import *
from PIL import ImageTk,Image #PIL -> Pillow
from tkinter import messagebox
import pandas as pd
from datetime import datetime

# ------------------------------------------------------------------------------------------------------------
# Tkinter Functions & Data
# ------------------------------------------------------------------------------------------------------------
# Currency Symbols
class curr_dat:
    def curr_rates():
        url = 'https://www.x-rates.com/table/?from=INR&amount=1'
        tables = pd.read_html(url)
        curr_list= list(tables[1].iloc[0:,0])
        curr_list.insert(18, 'Indian Rupees')
        f_rates = list(tables[1].iloc[0:,1])
        f_rates.insert(18, 1)
        inr_rates = list(tables[1].iloc[0:,2])
        inr_rates.insert(18, 1)
        
        # Create a sample DataFrame
        df = pd.DataFrame({'currency_name': curr_list, 'foreign_rates': f_rates, 'inr_rates': inr_rates})

        # Export DataFrame to a text file with tab-separated values (TSV)
        date = datetime.now().strftime('%Y-%m-%d')
        df['date'] = date
        l_update.config(text= f'Last Updated: {date}')
        df.to_csv('output.txt', sep='\t', index=False)

    def curr_sym(given = None):                     # Currency Symbols
        global sym
        sym = ['ARS', 'AUD', 'BHD', 'BWP', 'BRL', 'BND', 'BGN', 'CAD', 'CLP', 'CNY', 'COP', 'CZK', 'DKK', 'EUR', 'HKD', 
            'HUF', 'ISK', 'IDR', 'INR', 'IRR', 'ILS', 'JPY', 'KZT', 'KRW', 'KWD', 'LYD', 'MYR', 'MUR', 'MXN', 'NPR', 'NZD', 
            'NOK', 'OMR', 'PKR', 'PHP', 'PLN', 'QAR', 'RON', 'RUB', 'SAR', 'SGD', 'ZAR', 'LKR', 'SEK', 'CHF', 'TWD', 
            'THB', 'TTD', 'TRY', 'AED', 'GBP', 'USD', 'VES']
        if given is not None:
            return given
        else:
            return sym[18]   


# SWAP Function
def swap():
    btn1_text = curr1_btn.cget('text')
    btn2_text = curr2_btn.cget('text')
    curr1_btn.config(text= btn2_text)
    amt1.delete(0, END)
    curr2_btn.config(text= btn1_text)
    res_label.config(text= '')


# Calculate Function
def calc():
    btn1_xrate = f_rates[sym.index(curr1_btn.cget('text'))]
    btn1_yrate = inr_rates[sym.index(curr1_btn.cget('text'))]
    btn2_xrate = f_rates[sym.index(curr2_btn.cget('text'))]
    btn2_yrate = inr_rates[sym.index(curr2_btn.cget('text'))]
    amount = float(amt1.get())

    if (curr1_btn.cget('text')) == 'INR' and (curr2_btn.cget('text')) == 'INR':
        sum = float(btn1_xrate) * amount
    elif (curr1_btn.cget('text')) == 'INR' and (curr2_btn.cget('text')) != 'INR':
        sum = float(btn2_xrate) * amount
    elif (curr1_btn.cget('text')) != 'INR' and (curr2_btn.cget('text')) == 'INR':
        sum = float(btn1_yrate) * amount
    else:
        sum = (float(btn1_yrate)/float(btn2_yrate)) * amount
    
    sum = str(round(sum, 3))
    res_label.config(text= sum)



# Listbox Function
def curr_select(cs):
    if cs == 1:
        x, y, rh, rw = 0.13, 0.5, 0.35, 0.36
    else:
        x, y, rh, rw = 0.51, 0.5, 0.35, 0.36

    temp_frame = Frame(root, bg= '#18ADAD', bd= 4, relief= 'sunken')
    temp_frame.place(relx= x, rely= y, relheight= rh, relwidth= rw)
    def on_select(event):
        selected = listbox.get(listbox.curselection())
        curr_dat.curr_sym(selected)
        if cs == 1:
            btn1_text = sym[curr_list.index(selected)]
            curr1_btn.config(text=btn1_text)
        else:
            btn2_text = sym[curr_list.index(selected)]
            curr2_btn.config(text=btn2_text)
        root.after(100, lambda: [listbox.destroy(), temp_frame.place_forget()])  # Destroy the listbox after 0.1 second

    options = curr_list
    global listbox
    scrollbar = Scrollbar(temp_frame, orient=VERTICAL)
    listbox = Listbox(temp_frame, bg= '#18ADAD', width= 43, height=10, font= 'Calibri 14')
    scrollbar.config(command=listbox.yview)
    for option in options:
        listbox.insert(END, option)
    listbox.bind('<<ListboxSelect>>', on_select)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack()



# ------------------------------------------------------------------------------------------------------------
# Tkinter Canvas
# ------------------------------------------------------------------------------------------------------------

root = Tk()
root.title("Currency Calculator")
root.minsize(width=800,height=600)
root.maxsize(width=800,height=600)
root.geometry("800x600")

bg_image =Image.open("mainbg.png").resize((1366, 768),Image.ANTIALIAS)
img = ImageTk.PhotoImage(bg_image)
Canvas1 = Canvas(root)
Canvas1.create_image(683,384,image = img)      
Canvas1.config(bg="white",width = 800, height = 600)
Canvas1.pack(expand=True,fill=BOTH)


global curr_list, f_rates, inr_rates

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('output.txt', sep='\t', usecols=['currency_name', 'foreign_rates', 'inr_rates', 'date'])
curr_list = df['currency_name'].to_list()
f_rates = df['foreign_rates'].to_list()
inr_rates = df['inr_rates'].to_list()
date = df['date'].to_list()


# ------------------------------------------------------------------------------------------------------------
# Tkinter Interface
# ------------------------------------------------------------------------------------------------------------
# Refresh Button -- Refreshes the currency exchange rates 
ref_img = Image.open('refresh.png')
ref_img = ref_img.resize((110, 85),Image.ANTIALIAS)
ref_img = ImageTk.PhotoImage(ref_img)
refresh_btn = Button(root, image= ref_img, command= curr_dat.curr_rates)
refresh_btn.place(relx= .01, rely= .12, relheight= 0.06, relwidth= .12)

# Last Updated Label
try:
    l_update = Label(root, text= f'Last Updated: {date[0]}', bg= '#18ADAD', fg= 'black', font= ('Calibri 12'))
except:
    l_update = Label(root, text= 'Last Updated: No Data...', bg= '#18ADAD', fg= 'black', font= ('Calibri 12'))
l_update.place(relx= 0.01, rely=0.19, relheight=0.05, relwidth= 0.23)

# Main Title
curr_title = Label(root, text = "Real-Time Currency Exchange Rates", bg= '#859ec7', fg= 'black', font=('Algerian 16 underline'), relief= 'ridge', borderwidth=6, highlightthickness=5, highlightbackground="gray", highlightcolor='gray')
curr_title.place(relx= 0.005, rely= 0.005, relheight= 0.09, relwidth= 0.995)

# Currency 1 Frame -- Currency button + Entry Widget
curr1_frame = Frame(root, bg= '#18ADAD', bd=10, relief= 'ridge')
curr1_frame.place(relx= .25, rely= .4, relheight= .1, relwidth= .32)
img_curr1 = Image.open('curr1.png')
img_curr1 = img_curr1.resize((21, 21),Image.ANTIALIAS)
img_curr1 = ImageTk.PhotoImage(img_curr1)
curr1_btn_text = curr_dat.curr_sym(None)
curr1_btn = Button(curr1_frame, text= curr1_btn_text,font= 'Calibri 13', image= img_curr1, compound= 'right', command= lambda: curr_select(1))
curr1_btn.place(relx= .03, rely= .1, relheight= 0.8, relwidth= .25)
amt1 = Entry(curr1_frame, font= 'Calibri 14')
amt1.place(relx= .33, rely= .1, relheight= .8, relwidth= .64)

# Currency 2 Frame -- Currency button + Entry Widget
curr2_frame = Frame(root, bg= '#18ADAD', bd=10, relief= 'ridge')
curr2_frame.place(relx= .63, rely= .4, relheight= .1, relwidth= .12)
img_curr2 = Image.open('curr1.png')
img_curr2 = img_curr2.resize((21, 21),Image.ANTIALIAS)
img_curr2 = ImageTk.PhotoImage(img_curr2)
curr2_btn = Button(curr2_frame, text= 'USD',font= 'Calibri 13', image= img_curr2, compound= 'right', command= lambda: curr_select(2))
curr2_btn.place(relx= .03, rely= .1, relheight= 0.8, relwidth= .97)

# SWAP Button
swap_img = Image.open('swap.png')
swap_img = swap_img.resize((35, 35),Image.ANTIALIAS)
swap_img = ImageTk.PhotoImage(swap_img)
swap_btn = Button(root, image= swap_img, command= swap)
swap_btn.place(relx=.575, rely= .4, relheight=.1, relwidth=.05)

# Result Label
res_label = Label(root, text= '', bg= '#d1d0cd', fg= 'black', font=('Algerian 14'), relief= 'sunken', borderwidth= 3)
res_label.place(relx= 0.35, rely= 0.55, relheight= 0.07, relwidth= 0.3)

# Calculate Button
cal_img = Image.open('calculate.png')
cal_img = cal_img.resize((240, 90),Image.ANTIALIAS)
cal_img = ImageTk.PhotoImage(cal_img)
cal_btn = Button(root, image= cal_img, command= calc)
cal_btn.place(relx= .36, rely= .7, relheight= 0.08, relwidth= .28)

root.mainloop()