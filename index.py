from tkinter import ttk
from tkinter import *
from bs4 import BeautifulSoup
import requests
import sqlite3

root = Tk()
root.title("Game Backlog")

# Maximize the window screen
root.geometry("%dx%d" % (525, 360))
root.resizable(True, True)

#set window color
root['background']='#404040'

conn = sqlite3.connect("games.db")

# Create a cursor
cursor = conn.cursor()

# Button
round = PhotoImage(file='button.png')
show = PhotoImage(file='show.png')
add = PhotoImage(file='add.png')

def find_game(name):

    scrape = Tk()
    scrape.title("Game Selection")
    scrape['background']='#404040'
    scrape.geometry("%dx%d" % (815, 350))
    
    Game = scrape_game_input.get()
    game = Game.lower().replace(" ", "")
    
    html = requests.get("https://isthereanydeal.com/search/?q=" + game)
    soup = BeautifulSoup(html.text, "lxml")
    link_dict = {}
    link_list = []

    games_panels = soup.find_all("a", class_ = "card__title")
    games_lists = games_panels
    
    links_panels = soup.find_all("a", href=True)
    links = [panel.text.strip() for panel in links_panels]
    links_lists = links

    game_name = soup.find("h1")
    print(game_name.text)
    
    text_game = Label(scrape, text=game_name.text, bg='#404040', fg='#FFFFFF')
    text_game.pack(pady=(10,0))
    
    txt_output = Listbox(scrape, height=15, width=100, bg='#B3B3B3', highlightthickness=0, highlightbackground='#404040', borderwidth=0)
    scrollbar = Scrollbar(scrape)
    txt_output.pack(side='left', fill='y')
    scrollbar.configure(command=txt_output.yview)
    scrollbar.pack(side="right", fill="y")
    txt_output.configure(yscrollcommand=scrollbar.set)
    
    i = 0

    for game in games_lists:
        if i >= len(games_lists):
            break
            
        link = "https://isthereanydeal.com" + game.get('href')
        found_name = game.text.strip()
        link_dict[found_name] = link
        link_values = link_dict.values()
        link_list.append(game.text.strip() + " " + link)
        i += 1

    for link in link_list:
        txt_output.insert('end', link)
        
    txt_output.config(yscrollcommand=scrollbar.set)

    def on_select(event):
        selected_item = txt_output.get(txt_output.curselection())  # Get the selected item
        selected_link = selected_item.split()[-1]  # Extract the game name from the selected item
        print(selected_link)
    
        if selected_link in link_values:
            # Use selected_link as needed, e.g., open a web page, print it, etc.
            print("Selected link: " + selected_link)
            price_list = find_price(selected_link)

    txt_output.bind('<<ListboxSelect>>', on_select)  # Bind the event to the on_select function

    scrape.mainloop()


def submit():
    games_list = find_game(scrape_game_input.get())
    
def database_add():
    conn = sqlite3.connect("games.db")
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Insert into table
    cursor.execute("INSERT INTO games VALUES (:game_name, :game_console, :game_publisher, :year_released)",
                   {
                       'game_name': name_input.get(),
                       'game_console': console_input.get(),
                       'game_publisher': publisher_input.get(),
                       'year_released': year_input.get()
                   })
    
    name_input.delete(0, END)
    console_input.delete(0, END)
    publisher_input.delete(0, END)
    year_input.delete(0, END)
    
    conn.commit()

    conn.close()
    
def show_games():
    gamedb = Tk()
    gamedb.title("Game Selection")
    gamedb['background']='#404040'
    gamedb.geometry("%dx%d" % (815, 250))
    
    cursor.execute("SELECT *, oid FROM games")
    records = cursor.fetchall()
    tree = ttk.Treeview(gamedb, column=("c1", "c2", "c3", "c4"), show="headings")
    
    for record in records:
        print(record)
        tree.insert("", END, values=record)
        
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="Name")
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="Console")
    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="Publisher")
    tree.column("#4", anchor=CENTER)
    tree.heading("#4", text="Released")
    tree.pack()
    
    print(records)
    
def find_price(selected_link):

    scrape = Tk()
    scrape.title("Game Prices")
    scrape['background']='#404040'
    
    Game = scrape_game_input.get()
    game = Game.lower().replace(" ", "")
    
    html = requests.get(selected_link)
    soup = BeautifulSoup(html.text, "lxml")
    
    game_list = []

    price_panels = soup.find_all("td", class_ = "priceTable__new t-st3__price")
    prices = [panel.text.strip() for panel in price_panels]
    prices_list = prices

    shop_panels = soup.find_all("td", class_ = "priceTable__shop")
    shops = [panel.text.strip() for panel in shop_panels]
    shops = set(shops)

    game_name = soup.find("h1")
    print(game_name.text)
    
    text_game = Label(scrape, text=game_name.text, bg='#404040', fg='#FFFFFF')
    text_game.grid(row=1, column=0, pady=(10,0))
    
    txt_output = Text(scrape, height=5, width=30, bg='#B3B3B3', highlightthickness=0, highlightbackground='#404040', borderwidth=0)
    txt_output.grid(row=3, pady=10)

    i = 0
    
    for shop in shops:
        if (i > len(prices_list)):
            break
    
        game_list.append(shop + " " + prices_list[i])
        i += 1
        
    for game in game_list:
        txt_output.insert(END, game + "\n")

    scrape.mainloop()
    

# Add entry boxes
name_lable = Label(root, text="Name", anchor="w", justify="left", bg='#404040', fg='#FFFFFF')
name_input = Entry(root, width=47, bg='#B3B3B3', highlightthickness=0, highlightbackground='#404040', borderwidth=0)
console_lable = Label(root, text="Console", anchor="w", justify="left", bg='#404040', fg='#FFFFFF')
console_input = Entry(root, width=47, bg='#B3B3B3', highlightthickness=0, highlightbackground='#404040', borderwidth=0)
publisher_lable = Label(root, text="Publisher", anchor="w", justify="left", bg='#404040', fg='#FFFFFF')
publisher_input = Entry(root, width=47, bg='#B3B3B3', highlightthickness=0, highlightbackground='#404040', borderwidth=0)
year_lable = Label(root, text="Year", anchor="w", justify="left", bg='#404040', fg='#FFFFFF')
year_input = Entry(root,width=47, bg='#B3B3B3', highlightthickness=0, highlightbackground='#404040', borderwidth=0)
scrape_game_lable = Label(root, text="Find a game", anchor="w", justify="left", bg='#404040', fg='#FFFFFF')
scrape_game_input = Entry(root, width=47, bg='#B3B3B3', highlightthickness=0, highlightbackground='#404040', borderwidth=0)

# Create empty row

# Add buttons
button_add = Button(root, text="Add game to database", image=add, border=0, bg='#404040', highlightthickness=0, highlightbackground='#404040', activebackground='#404040', command=database_add)
button_show = Button(root, text="Show games", image=show, border=0, bg='#404040', highlightthickness=0, highlightbackground='#404040', activebackground='#404040', command=show_games)
button_scrape = Button(root, image=round, border=0, borderwidth=0, command=submit, bg='#404040', highlightthickness=0, highlightbackground='#404040', activebackground='#404040')

# Pack entries
name_lable.grid(row=1, column=0, sticky=W, padx=(20,0))
name_input.grid(row=1, column=1, columnspan=2, padx=20, pady=(5, 0))
console_lable.grid(row=2, column=0, sticky=W, padx=(20,0))
console_input.grid(row=2, column=1, columnspan=2, padx=20)
publisher_lable.grid(row=3, column=0, sticky=W, padx=(20,0))
publisher_input.grid(row=3, column=1, columnspan=2, padx=20)
year_lable.grid(row=4, column=0, sticky=W, padx=(20,0))
year_input.grid(row=4, column=1, columnspan=2, padx=20, pady=(0,5))
scrape_game_lable.grid(row=9, column=0, sticky=W, padx=(20,0))
scrape_game_input.grid(row=9,column=1, columnspan=2, pady=(5, 5))

#Header
header1 = Label(root, text="Game Backlog", font=18, bg='#404040', fg='#FFFFFF')
header1.grid(row=0, column=1, columnspan=2)
header2 = Label(root, text="Search for Deals", font=18, bg='#404040', fg='#FFFFFF')
header2.grid(row=8, column=1, columnspan=2)

# Pack buttons
button_add.grid(row=5, column=1, sticky=W, padx=(20,0))
button_show.grid(row=5, column=2, sticky=E, padx=(0,20))
button_scrape.grid(row=10, column=1, columnspan=2)

# Separator
separator = ttk.Separator(root, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky=EW, pady=20)

root.mainloop()
