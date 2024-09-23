import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk, PhotoImage, Label, Button, Entry, Listbox, Scrollbar, Canvas, Frame, Toplevel
from datetime import *
import csv
from rec1 import *
import threading


class InvoiceGenerator(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Generate Invoice")
        self.geometry("800x550")
        self.cart = LinkedList()
        # data format: (customer_name, contact_number, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), medicine_name, quantity, total_price)
        self.configure(bg="black")

        self.label = tk.Label(self, text="Invoice Generator", bg="black", fg="white", font=("Arial", 18))
        self.label.pack(pady=10)

        # Labels and Entry fields with a light beige background
        self.name_label = tk.Label(self, text="Customer Name", bg="black")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.contact_label = tk.Label(self, text="Contact Number", bg="black")
        self.contact_label.pack()
        self.contact_entry = tk.Entry(self)
        self.contact_entry.pack()

        self.date_label = tk.Label(self, text="Date and Time", bg="black")
        self.date_label.pack()
        self.date_entry = tk.Entry(self)
        self.date_entry.pack()
        self.update_date_time()

        self.medicine_label = tk.Label(self, text="Medicine Name", bg="black")
        self.medicine_label.pack()
        self.medicine_entry = tk.Entry(self)
        self.medicine_entry.pack()

        self.quantity_label = tk.Label(self, text="Quantity", bg="black")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.pack()

        # Buttons with a slightly darker shade for contrast
        self.add_button = tk.Button(self, text="Add to Cart", command=self.add_to_cart, bg="black")
        self.add_button.pack()

        self.cart_listbox = tk.Listbox(self)
        self.cart_listbox.pack()

        self.delete_button = tk.Button(self, text="Delete from Cart", command=self.delete_from_cart, bg="black")
        self.delete_button.pack()

        self.bill_button = tk.Button(self, text="Generate Bill", command=self.generate_bill, bg="black")
        self.bill_button.pack()

    def update_date_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, now)
        self.after(1000, self.update_date_time)  # Update every second

    def add_to_cart(self):
        # Get customer details
        customer_name = self.name_entry.get()
        contact_number = self.contact_entry.get()

        # Get medicine details
        medicine_name = self.medicine_entry.get()
        medicine_name = medicine_name.title()
        quantity_str = self.quantity_entry.get()

        try:
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.")
            return

        found = False
        current_node = ll.head
        while current_node:
            if current_node.data[1] == medicine_name:
                total_price = (float(current_node.data[6]) + float(current_node.data[7])) * quantity
                # Insert medicine with customer details
                self.cart.insert_at_end([customer_name, contact_number, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), medicine_name, quantity, total_price])
                self.cart_listbox.insert(tk.END, f"{medicine_name} - {quantity} - {total_price}")
                found = True
                break
            current_node = current_node.next

        if not found:
            messagebox.showerror("Error", "Medicine not found.")

    # Add this function to data_operations.py

    def save_medicines_to_file(self,file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for item in ll:
                writer.writerow(item)

    def delete_from_cart(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            count = 0
            current_node = self.cart.head
            while current_node:
                if count == selected_index[0]:
                    # Remove the selected item from the cart
                    self.cart.remove_at(count)
                    break
                current_node = current_node.next
                count += 1

            # Delete the selected item from the listbox
            self.cart_listbox.delete(selected_index)


    def generate_bill(self):
        self.save_to_csv()  # Save invoice details to CSV first

        total_amount = 0
        bill_details = ""
        current_node = self.cart.head
        while current_node:
            total_amount += int(current_node.data[5])
            bill_details += f"{current_node.data[3]} - {current_node.data[4]} - {current_node.data[5]}\n"
            current_node = current_node.next

        messagebox.showinfo("Bill", f"Total Amount: {total_amount}\n\nDetails:\n{bill_details}")
        self.update_stock()  # Now clear the cart and update stock


    def update_stock(self):
        current_node = self.cart.head
        while current_node:
            for med in ll:
                if med[1] == current_node.data[3]:  # Assuming the medicine name is at index 3
                    med[3] = int(med[3]) - current_node.data[4]  # Update the quantity in stock
                    break
            current_node = current_node.next

        # Clear the cart and the listbox displaying the cart items
        self.cart.clear()
        self.cart_listbox.delete(0, tk.END)
        self.save_medicines_to_file('medicine_data.csv')

    def save_to_csv(self):
        # Get customer details
        customer_name = self.name_entry.get()
        contact_number = self.contact_entry.get()
        purchase_date = datetime.now().strftime("%Y-%m-%d")
        purchase_time = datetime.now().strftime("%H:%M:%S")

        with open("invoices.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(["Customer Name", "Contact Number", "Date", "Time", "Medicine Name", "Quantity", "Total Price"])

            current_node = self.cart.head
            while current_node:
                # Extract data from linked list node
                medicine_name = current_node.data[3]
                quantity = current_node.data[4]
                total_price = current_node.data[5]

                # Write to CSV
                writer.writerow([customer_name, contact_number, purchase_date, purchase_time, medicine_name, quantity, total_price])
                current_node = current_node.next

        messagebox.showinfo("Success", "Invoice details saved to CSV file.")

def open_invoice_window():
    invoice_window = InvoiceGenerator(r)

def save_expired_to_csv():
    # removed date is the date in which expired med is deleted
    removed_date = datetime.now().strftime("%Y-%m-%d")

    with open("expired_med.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header if the file is empty
        if file.tell() == 0:
            writer.writerow(
                ["Medicine Name", "Removed Date", "Quantity", "Loss Amount"])

        for i in exp_med_list:
            writer.writerow(
                [i[0], removed_date, i[1], i[2]])

class SalesView(tk.Toplevel):
    def __init__(self, master=None, data=None, data2=None):
        super().__init__(master)
        self.data = data
        self.exp_data = data2
        self.title("Sales and Loss")
        self.geometry("600x400")

        # Parse dates and extract year, month, day
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data['Year'] = self.data['Date'].dt.year
        self.data['Month'] = self.data['Date'].dt.month
        self.data['Day'] = self.data['Date'].dt.day

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Date:").pack(pady=5)

        self.day = ttk.Combobox(self, values=[i for i in range(1, 32)], state="readonly")
        self.day.pack(pady=5)

        self.month = ttk.Combobox(self, values=[i for i in range(1, 13)], state="readonly")
        self.month.pack(pady=5)

        self.year = ttk.Combobox(self, values=list(self.data['Year'].unique()), state="readonly")
        self.year.pack(pady=5)

        tk.Button(self, text="Show Sales and loss", command=self.show_sales).pack(pady=20)

        self.result = tk.Label(self, text="", wraplength=700)
        self.result.pack(pady=20)

    def show_sales(self):
        day = self.day.get()
        month = self.month.get()
        year = self.year.get()

        filtered_data = self.data
        exp_med_data = self.exp_data


        if year:
            filtered_data = filtered_data[filtered_data['Year'] == int(year)]
            exp_med_data = exp_med_data[exp_med_data['Year'] == int(year)]
        if month:
            filtered_data = filtered_data[filtered_data['Month'] == int(month)]
            exp_med_data = exp_med_data[exp_med_data['Month'] == int(month)]
        if day:
            filtered_data = filtered_data[filtered_data['Day'] == int(day)]
            exp_med_data = exp_med_data[exp_med_data['Day'] == int(day)]

        if day or month or year:
            filtered_data['Total Price'] = pd.to_numeric(filtered_data['Total Price'], errors='coerce')
            total_sales = filtered_data['Total Price'].sum()
            total_medicines = filtered_data['Quantity'].sum()

            result_text = f"Total Sales : {total_sales}\nTotal Medicines Sold: {total_medicines}"

            exp_med_data['Loss Amount'] = pd.to_numeric(exp_med_data['Loss Amount'], errors='coerce')
            exp_med_data['Product'] = exp_med_data['Loss Amount'] * exp_med_data['Quantity']
            total_loss = exp_med_data['Product'].sum()
            total_del_medicines = exp_med_data['Quantity'].sum()

            result_text += f"\n\nTotal expired medicines: {total_del_medicines}"
            result_text += f"\nLoss Amount: {total_loss}"

            self.result.config(text=result_text)

def open_sales_view():
    data = pd.read_csv('invoices.csv')
    exp_data = pd.read_csv('expired_med.csv')

    exp_data["Removed Date"] = pd.to_datetime(exp_data["Removed Date"])
    exp_data["Year"] = exp_data["Removed Date"].dt.year
    exp_data["Month"] = exp_data["Removed Date"].dt.month
    exp_data["Day"] = exp_data["Removed Date"].dt.day

    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day

    SalesView(data=data,data2=exp_data)

class Locate_bin():
#functions for locate bin menu option
    def find_bin(self, event=None):
        global medname_entry, disp, disp_notfound
        medname = medname_entry.get().title()

        if 'disp' in globals() and disp:
            disp.destroy()
        if 'disp_notfound' in globals() and disp_notfound:
            disp_notfound.destroy()

        found = False
        for i in range(1, 21):
            if medname in meds_dict[i]:
                disp = Label(top_level, text="bin {}".format(i), bg='#BCD2EE',
                             font=('Garamond', 20, 'bold'))
                disp.place(relx=0.75, y=180, anchor='center')
                found = True
                break

        if not found:
            disp_notfound = Label(top_level, text="Medicine not found", bg='#BCD2EE', font=('Garamond', 17, 'bold'))
            disp_notfound.place(relx=0.75, x=25, y=180, anchor='center')


    def select_listbox(self, event): # to select a medicine from the list box when user clicks on it
        selection = lib.curselection()
        if selection:
            selected_med = lib.get(selection)
            medname_entry.delete(0, END)
            medname_entry.insert(0, selected_med)
            self.find_bin()


    def check_bin(self, event):
        medname = medname_entry.get()

        if medname=='':
            data=medlist
        else:
            data=[med for med in medlist if medname.lower() in med.lower()]
        self.medlistbox(data)

    def medlistbox(self, data):
        lib.delete(0, END)
        for med in data:
            lib.insert(END, med)

    def locate_exit(self):
        msg_box=messagebox.askyesno(title='Exit', message='Are you sure you want to exit?',)
        if msg_box:
            top_level.destroy()
        else:
            top_level.lift(r)

    def locate(self): # fist function that is called from the main menu
        global medname_entry,top_level, image_loc, lib, search_img
        big_image_loc = PhotoImage(file="Pic home.png")
        image_loc = big_image_loc.subsample(20, 20)
        search_big_img = PhotoImage(file="search_img.png")
        search_img= search_big_img.subsample(20,20)

        #Creating top level window for the locate bin option
        top_level=Toplevel(r)
        top_level.title('Locate Medicine')
        top_level.geometry('1000x700+250+60')
        top_level.configure(bg='#BCD2EE')

        #Adding home button
        home_button = Button(top_level, text='Home', font=('Garamond', 13, 'bold'),
                             image=image_loc, compound=LEFT, bd=6, command=self.locate_exit,
                             relief='ridge').place(relx=1, x=-120, y=20,width=100, height=50)

        #Main heading to the window
        Heading = Label(top_level, text='Locate Medicine', bg='#BCD2EE',
                        font=('Garamond', 60, 'bold')).place(x=500, y=70, anchor='center')

        #Search Image
        search=Button(top_level, image=search_img, command=self.find_bin).place(relx=0.25, x=90, y= 180, anchor='center')

        #Entry box to take the input of the
        medname_entry = Entry(top_level, font=('Garamond', 15))
        medname_entry.place(relx=0.5, y=180 ,anchor='center', width=275)
        medname_entry.bind('<Return>', self.find_bin)
        medname_entry.bind('<KeyRelease>', self.check_bin)

        #Adding the list box to show serch and narrow the result
        lib=Listbox(top_level, font=('Garamond', 15))
        lib.place(relx=0.5, y=200, anchor='n', width=250, height=120)
        self.medlistbox(medlist)
        lib.bind('<<ListboxSelect>>', self.select_listbox)

        #Scrollbar for listbox
        scrollbar = Scrollbar(top_level, orient="vertical", command=lib.yview)
        lib.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=0.5, x=125, y=200, height=120)

        #Creating tree table to display bins with the medicines as the children
        table_bin=ttk.Treeview(top_level, columns=('bin'), style='parent.Treeview')
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Garamond', 15, 'bold')) #To change text formatting for headings
        table_bin.tag_configure("parent", font=("Garamond", 12, "bold"))
        table_bin.tag_configure("child", font=("Garamond", 12))
        table_bin.heading('bin', text='Bin No.')
        table_bin.column('bin', width=250)

        #changing width of first column containing arrows
        minwidth = table_bin.column('#0',option = 'minwidth')
        table_bin.column('#0',width = minwidth)
        binlist=[]
        for i in range (1, 21):
            binlist.append('Bin '+str(i))

        #inserting bins and the medicines in the tree
        for count, rec in enumerate(binlist):
            table_bin.insert('', 'end', text='', iid=count,  values=(rec,), tags=('parent',))
            for meds in range(len(meds_dict[count+1])):

                table_bin.insert(count, 'end', values=('            '+meds_dict[count+1][meds],), tags=('child',))

        table_bin.place(relx=0.5,y=350,anchor='n', height=275)

        #Scrollbar for treeview
        scrollbar = Scrollbar(top_level, orient="vertical", command=table_bin.yview)
        table_bin.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=625, y=350, height=275)


class Manage_stock:
    def managestock(self):
        global image_man, headline
        big_image=PhotoImage(file="Pic home.png")
        image_man=big_image.subsample(20,20)
        headline=Toplevel(r)
        headline.title("Manage Stock")
        headline.geometry("1200x680+150+50")

    #Add 2 frames to manage UI
        left_control=Frame(headline, bg='#BCD2EE')
        left_control.place(x=0, y=0, width=225, height=680)
        main_frame=Frame(headline, bg='white')
        main_frame.place(x=225, y=0, width=975, height=680)

    #Heading
        Heading =Label(main_frame, text='Stock', bg='white', fg='black', font=('Garamond', 50, 'bold'))
        Heading.place(x=450, y=50, anchor='center')

    #Home button
        home_button = Button(main_frame, text='Home', font=('Garamond', 13, 'bold'), image=image_man,
                             compound=LEFT, bd=6, command=self.check_exit, relief='ridge')
        home_button.place(relx=1, x=-120, y=20,width=100, height=50)


    #Button to check expiry date
        exp_check=Button(left_control, text="Check expiry date",
                         command=self.exp_window, font=('Garamond', 15 , 'bold'))
        exp_check.place(x=25, y=400, width=175, height=50)

    #Button to check stock
        stk_check=Button(left_control, text="Check stock",
                         command=self.check_stock, font=('Garamond', 15 , 'bold'))
        stk_check.place(x=25, y=250, width=175, height=50)

    #button to add medicine
        add_med=Button(left_control, text="Add Medicines",
                       command=self.add_med_window, font=('Garamond', 15 , 'bold'))
        add_med.place(x=25, y=100, width=175, height=50)

    #To create table to display a table
        table=ttk.Treeview(main_frame,columns=("c1","c2","c3","c4","c5","c6","c7","c8"),show="headings")
        style=ttk.Style()
        style.configure("Treeview.Heading", font=('Garamond', 15, 'bold')) #To change text formatting for headings
        table.tag_configure("parent", font=("Garamond", 12))

        table.heading("c1",text="medicine ID")
        table.heading("c2",text="medicine name")
        table.heading("c3",text="Expiry date")
        table.heading("c4",text="Quantity")
        table.heading("c5",text="Bin")
        table.heading("c6",text="Actual price")
        table.heading("c7",text="Selling price")
        table.heading("c8",text="GST")
        table.column('c1', width=120)
        table.column('c2', width=170)
        table.column('c3', width=145)
        table.column('c4', width=100)
        table.column('c5', width=65)
        table.column('c6', width=140)
        table.column('c7', width=135)
        table.column('c8', width=100)

        for i in ll:
            table.insert('', 'end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]), tags=('parent',))
        scrollbar = Scrollbar(headline, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        table.place(relx=0, y=80, height=600)
        scrollbar.place(relx=0.987, y=80, height=600)

    def check_exit(self):
        msg_box=messagebox.askyesno(title='Exit', message='Are you sure you want to exit?',)
        if msg_box:
            headline.destroy()
        else:
            headline.lift(r)


    def exp_window(self):
        global back_image
        big_image = PhotoImage(file="back button.png")
        back_image = big_image.subsample(10, 10)
        def exp_clicked():
            set_days=day_control.get()
            exp_med_list=[]
            today=date.today()
            for med in ll:
                exp_date=med[2].split('-')
                remain=(date(int(exp_date[0]), int(exp_date[1]), int(exp_date[2]))-today).days
                if remain<int(set_days):
                    exp_med_list.append([med[1], med[3], med[2], remain])
            if len(exp_med_list)!=0:
                exp_table=ttk.Treeview(exp_win,columns=("c1","c2","c3","c4"),show="headings")
                exp_table.heading("c1",text="Medicine name")
                exp_table.heading("c2",text="Quantity")
                exp_table.heading("c3",text="Expairy date")
                exp_table.heading("c4",text="Remaining days")
                exp_table.column('c1', width=140)
                exp_table.column('c2', width=90)
                exp_table.column('c3', width=150)
                exp_table.column('c4', width=150)

                for med in exp_med_list:
                    exp_table.insert('', 'end', values=(med[0], med[1], med[2], med[3]))
                scrollbar = Scrollbar(exp_win, orient="vertical", command=exp_table.yview)
                exp_table.configure(yscrollcommand=scrollbar.set)

                exp_table.place(relx=0.5, y=250, anchor='center', height=200)
                scrollbar.place(relx=0.825, y=150, height=200)
            else:
                messagebox.showinfo("Expiry Date", f"No medicines with expiry date within {set_days} days")
            headline.lift(r)
            exp_win.lift(headline)
        def check_back():
            msg_box = messagebox.askyesno(title='Exit', message='Are you sure you want to go back?', )
            if msg_box:
                exp_win.destroy()
                headline.lift(r)
            else:
                headline.lift(r)
                exp_win.lift(headline)
        exp_win=Toplevel(headline, bg='#BCD2EE')
        exp_win.geometry('800x400+350+200')
        days=IntVar()
        Heading=Label(exp_win, text='Expiry date', bg='#BCD2EE', font=("Garamond", 40, 'bold'))
        Heading.place(relx=0.5, y=50, anchor='center')

        sub=Label(exp_win, text='Medicines that expire within           days:',
                  font=("Garamond", 20), bg='#BCD2EE')
        sub.place(relx=0.5, y=100, anchor='center')
        day_control=ttk.Combobox(exp_win, textvariable=days,
                                 font = ('Garamond',12), values= (10, 30, 60, 90))
        day_control.place(x=525, y=100, width=50, height=20, anchor='center')
        done_button = Button(exp_win, text = 'done', command =exp_clicked)
        done_button.place(relx=0.8,y=100, anchor='center')
        # back button
        back_button = Button(exp_win, text='Back', font=('Garamond', 13, 'bold'), image=back_image, bg='white',
                             compound=LEFT, bd=6, command=check_back, relief='ridge')
        back_button.place(relx=1, x=-120, y=20, width=100, height=50)

    def check_stock(self):
        global back_image
        big_image = PhotoImage(file="back button.png")
        back_image = big_image.subsample(10, 10)
        def check_stock_clicked():
            set_quantity = quantity_control.get()
            low_stock_list = [med for med in ll if int(med[3]) < int(set_quantity)]
            if low_stock_list:
            # Create a Treeview to display low stock medicines
                low_stock_table = ttk.Treeview(low_stock_window, columns=("ID", "Name", "Quantity"), show="headings")
                low_stock_table.heading("ID", text="ID")
                low_stock_table.heading("Name", text="Name")
                low_stock_table.heading("Quantity", text="Quantity")
                low_stock_table.column('ID', width=100)
                low_stock_table.column('Name', width=300)
                low_stock_table.column('Quantity', width=150)

                for med in low_stock_list:
                    low_stock_table.insert('', 'end', values=(med[0], med[1], med[3]))

                scrollbar = Scrollbar(low_stock_window, orient="vertical", command=low_stock_table.yview)
                low_stock_table.configure(yscrollcommand=scrollbar.set)

                low_stock_table.place(relx=0.5, y=250, anchor='center', height=200)
                scrollbar.place(relx=0.825, y=150, height=200)

            else:
                messagebox.showinfo("Low Stock", f"No medicines with quantity less than {set_quantity} units.")
            headline.lift(r)
            low_stock_window.lift(headline)
        def check_back():
            msg_box = messagebox.askyesno(title='Exit', message='Are you sure you want to go back?', )
            if msg_box:
                low_stock_window.destroy()
                headline.lift(r)
            else:
                headline.lift(r)
                low_stock_window.lift(headline)
    # Create a new window to display low stock medicines
        low_stock_window = Toplevel(headline, bg='#BCD2EE')
        low_stock_window.title("Low Stock Medicines")
        low_stock_window.geometry("800x400+300+200")

        Heading = Label(low_stock_window, text='Low Stock Medicines', bg='#BCD2EE', font=("Garamond", 40, 'bold'))
        Heading.place(relx=0.5, y=50, anchor='center')

        sub = Label(low_stock_window, text='Medicines with quantity less than:',
                font=("Garamond", 20), bg='#BCD2EE')
        sub.place(relx=0.5, x=-30, y=100, anchor='center')
        quantity = IntVar()
        quantity_control = ttk.Combobox(low_stock_window, textvariable=quantity,
                                    font=('Garamond', 12), values=(50, 100))
        quantity_control.place(x=575, y=100, width=50, height=20, anchor='center')
        done_button = Button(low_stock_window, text='Done', command=check_stock_clicked)
        done_button.place(relx=0.8, y=100, anchor='center')
        #back button
        back_button = Button(low_stock_window, text='Back', font=('Garamond', 13, 'bold'), image=back_image, bg='white',
                             compound=LEFT, bd=6, command=check_back, relief='ridge')
        back_button.place(relx=1, x=-120, y=20, width=100, height=50)
    def add_med_window(self):
        add_window = Toplevel(headline, bg='#BCD2EE')
        add_window.title("Add or Update Medicine")
        add_window.geometry("400x300")

        Button(add_window, text="Update Medicine", command=self.update_medicine).pack(pady=10)
        Button(add_window, text="Add New Medicine", command=self.add_new_medicine).pack(pady=10)

    def update_medicine(self):
        update_window = Toplevel(headline)
        update_window.title("Update Medicine")
        update_window.geometry("300x200")

        Label(update_window, text="Medicine Name:").pack()
        med_name_entry = Entry(update_window)
        med_name_entry.pack()

        Label(update_window, text="Increment Quantity:").pack()
        quantity_entry = Entry(update_window)
        quantity_entry.pack()

        def find_and_update():
            med_name = med_name_entry.get()
            for med in ll:
                if med[1] == med_name:
                    try:
                        increment = int(quantity_entry.get())
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid quantity.")
                        return
                    med[3] = int(med[3]) + increment
                    self.update_csv()
                    messagebox.showinfo("Success", "Medicine quantity updated.")
                    return
            messagebox.showinfo("Not Found", "Medicine not available.")

        Button(update_window, text="Update", command=find_and_update).pack()

    def add_new_medicine(self):
        add_new_window = Toplevel(headline)
        add_new_window.title("Add New Medicine")
        add_new_window.geometry("400x400")

        Label(add_new_window, text="Medicine Name:").pack()
        med_name_entry = Entry(add_new_window)
        med_name_entry.pack()

        Label(add_new_window, text="Expiry Date (YYYY-MM-DD):").pack()
        exp_date_entry = Entry(add_new_window)
        exp_date_entry.pack()

        Label(add_new_window, text="Quantity:").pack()
        quantity_entry = Entry(add_new_window)
        quantity_entry.pack()

        Label(add_new_window, text="Bin Number:").pack()
        bin_entry = Entry(add_new_window)
        bin_entry.pack()

        Label(add_new_window, text="Cost Price:").pack()
        cost_price_entry = Entry(add_new_window)
        cost_price_entry.pack()

        Label(add_new_window, text="Selling Price:").pack()
        selling_price_entry = Entry(add_new_window)
        selling_price_entry.pack()

        Label(add_new_window, text="GST:").pack()
        gst_entry = Entry(add_new_window)
        gst_entry.pack()

        def save_new_medicine():
            med_id = len(ll) + 1001
            med_name = med_name_entry.get()
            exp_date = exp_date_entry.get()
            try:
                quantity = int(quantity_entry.get())
                bin_number = bin_entry.get()
                cost_price = float(cost_price_entry.get())
                selling_price = float(selling_price_entry.get())
                gst = float(gst_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid data.")
                return

            new_med = [med_id, med_name, exp_date, quantity, bin_number, cost_price, selling_price, gst]
            ll.insert_at_end(new_med)
            self.update_csv()
            messagebox.showinfo("Success", "New medicine added.")
            add_new_window.destroy()

        Button(add_new_window, text="Add Medicine", command=save_new_medicine).pack()

    def update_csv(self):
        with open('medicine_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(ll)


def main_exit():
    msg_box=messagebox.askyesno(title='Exit', message='Are you sure you want to exit the application?',)
    if msg_box:
        r.destroy()

exp_med_list = []


def menu(r):
    global image
    big_image = PhotoImage(file="exit pic.png")
    image = big_image.subsample(10, 10)

    Heading = Label(r, text='MediTrack', font=('Garamond', 60, 'bold'), fg='black', bg='#f5f5f5')
    Heading.place(relx=0.5, y=70, anchor='center')

    SHeading = Label(r, text='Pharmacy Inventory and Sales Management System', font=('Garamond', 25, 'bold'),
                     fg='black', bg='#f5f5f5')
    SHeading.place(relx=0.5, y=130, anchor='center')

    exit_button = Button(r, text='  EXIT', font=('Garamond', 15, 'bold'), image=image, compound='left', bd=6,
                         command=main_exit, relief='ridge')
    exit_button.place(relx=1, x=-250, y=50, width=200, height=70)

    button1 = Button(r, text='VIEW SALES AND LOSS', font=('Garamond', 20, 'bold'), bg='#BCD2EE', bd=6,
                     command=open_sales_view, relief='ridge')
    button1.place(relx=0.25, rely=0.25, y=130, width=300, height=125, anchor='center')

    button2 = Button(r, text='MANAGE STOCK', font=('Garamond', 20, 'bold'), bg='#BCD2EE', bd=6,
                     command=man_stk.managestock, relief='ridge')
    button2.place(relx=0.75, rely=0.25, y=130, width=300, height=125, anchor='center')

    button3 = Button(r, text='GENERATE INVOICE', font=('Garamond', 20, 'bold'), bg='#BCD2EE', bd=6,
                     command=open_invoice_window, relief='ridge')
    button3.place(relx=0.25, rely=0.75, width=300, height=125, anchor='center')

    button4 = Button(r, text='LOCATE MEDICINE', font=('Garamond', 20, 'bold'), bg='#BCD2EE', bd=6,
                     command=loc_bin.locate, relief='ridge')
    button4.place(relx=0.75, rely=0.75, width=300, height=125, anchor='center')

    # Remove medicines which have expired
    today = date.today()
    for med in ll:
        exp_date = med[2].split('-')
        remain = (date(int(exp_date[0]), int(exp_date[1]), int(exp_date[2])) - today).days
        if remain < 0:
            exp_med_list.append([med[1], med[3], med[5]])
            save_expired_to_csv()

    if len(exp_med_list) > 0:
        if len(exp_med_list) == 1:
            def exp1():
                messagebox.showinfo(title='Expired', message=f'{exp_med_list[0][0]} has expired')

            timer = threading.Timer(0.5, exp1)
        else:
            meds = '\n'.join([med[0] for med in exp_med_list])

            def exp2():
                messagebox.showinfo(title='Expired', message=f'The following medicines have expired:\n{meds}')

            timer = threading.Timer(0.5, exp2)

        timer.start()
    if len(exp_med_list) != 0:
        i = -1;
        indices = []
        for med_exp in exp_med_list:
            for medicine in ll:
                i += 1
                if med_exp[0] == medicine[1]:
                    indices.append(i)
        for j in indices:
            ll.remove_at(j)
        med_del = open('medicine_data.csv', 'w', newline='')
        writer = csv.writer(med_del)
        for meds in ll:
            writer.writerow(meds)
        f.close()

    # Removing expired medicines from the list
    expired_names = [med[0] for med in exp_med_list]
    updated_ll = [med for med in ll if med[1] not in expired_names]

    with open('medicine_data.csv', 'w', newline='') as med_del:
        writer = csv.writer(med_del)
        for med in updated_ll:
            writer.writerow(med)

medlist=[]
for med in meds_dict:
    medlist+=meds_dict[med]
loc_bin = Locate_bin()
man_stk = Manage_stock()

r = tk.Tk()
r.title('Medi Track')
r.geometry('6000x4000+0+0')
canvas = Canvas(width=6000, height=4000)
image_path = PhotoImage(file="pexels-skelm-7856722.png")
canvas.create_image(730, 400, image=image_path)
canvas.place(x=0, y=0)

menu(r)
r.mainloop()
