from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import ttk
import webbrowser
import textwrap


#Variable to keep track of the index of the article in display, for displaying different articles as only 10 fit on the gui at one time
headline_tally = 0

#Fonts and cursors for gui
title_font = ("Helvetica", 12, "underline", "bold")
title_cursor = "hand2"

#takes links and subtext from soup and makes a list of dictionaries for each news article with a score of over 150 points
#to change from 150 to a lower or higher number you can just change the 150 value directly as it appears no where else
def alternative_hacker_news(links, subtext):
    hn = []
    for inx, item in enumerate(links):
        vote = subtext[inx].select(".score")


        title = links[inx].getText()
        href = links[inx].get("href", None)
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > 150:
                hn.append({"title": title, "link": href, "score": points})

    return hn


#Sorts the list of dictionaries from alternative_hacker_news to be ordered by score (highest first)
def sort_by_points(hn_list):
    sorted_list = sorted(hn_list, key=lambda k: k["score"], reverse=True)

    return sorted_list


#Formats the titles within the dictionaries in the sorted list so that they fit in the labels for titles on the gui
def format_titles(sorted_list):
    wrap_size = 30
    for dictionary in sorted_list:
        if len(dictionary["title"]) > wrap_size:
            dictionary["title"] = textwrap.fill(dictionary["title"], wrap_size)
    formatted_list = sorted_list

    return formatted_list


#Opens the links with the browser, activated when a title is clicked
def open_url(url):
    webbrowser.open_new(url)


#Binds the previous function onto each title so that they can simply be clicked to open the respective link
def bind_links(count, formatted_list):
    title_label1.bind("<Button-1>", lambda e: open_url(formatted_list[count]["link"]))
    title_label2.bind("<Button-1>", lambda e: open_url(formatted_list[count+1]["link"]))
    title_label3.bind("<Button-1>", lambda e: open_url(formatted_list[count+2]["link"]))
    title_label4.bind("<Button-1>", lambda e: open_url(formatted_list[count+3]["link"]))
    title_label5.bind("<Button-1>", lambda e: open_url(formatted_list[count+4]["link"]))
    title_label6.bind("<Button-1>", lambda e: open_url(formatted_list[count+5]["link"]))
    title_label7.bind("<Button-1>", lambda e: open_url(formatted_list[count+6]["link"]))
    title_label8.bind("<Button-1>", lambda e: open_url(formatted_list[count+7]["link"]))
    title_label9.bind("<Button-1>", lambda e: open_url(formatted_list[count+8]["link"]))
    title_label10.bind("<Button-1>", lambda e: open_url(formatted_list[count+9]["link"]))


#Sets the title for each of the 10 labels on the gui
#Titles set according to variable headline_tally, so they may be given in order
def set_titles(count, formatted_list):
    title_label1["text"] = f'{str(count+1)}.{formatted_list[count]["title"]}\nScore: {str(formatted_list[count]["score"])}'
    title_label2["text"] = f'{str(count+2)}.{formatted_list[count+1]["title"]}\nScore: {str(formatted_list[count+1]["score"])}'
    title_label3["text"] = f'{str(count+3)}.{formatted_list[count+2]["title"]}\nScore: {str(formatted_list[count+2]["score"])}'
    title_label4["text"] = f'{str(count+4)}.{formatted_list[count+3]["title"]}\nScore: {str(formatted_list[count+3]["score"])}'
    title_label5["text"] = f'{str(count+5)}.{formatted_list[count+4]["title"]}\nScore: {str(formatted_list[count+4]["score"])}'
    title_label6["text"] = f'{str(count+6)}.{formatted_list[count+5]["title"]}\nScore: {str(formatted_list[count+5]["score"])}'
    title_label7["text"] = f'{str(count+7)}.{formatted_list[count+6]["title"]}\nScore: {str(formatted_list[count+6]["score"])}'
    title_label8["text"] = f'{str(count+8)}.{formatted_list[count+7]["title"]}\nScore: {str(formatted_list[count+7]["score"])}'
    title_label9["text"] = f'{str(count+9)}.{formatted_list[count+8]["title"]}\nScore: {str(formatted_list[count+8]["score"])}'
    title_label10["text"] = f'{str(count+10)}.{formatted_list[count+9]["title"]}\nScore: {str(formatted_list[count+9]["score"])}'


#shows previous 10 articles (if possible)
def previous_button_function(formatted_list):
    global headline_tally
    if headline_tally >= 10:
        headline_tally -= 10
        set_titles(headline_tally, formatted_list)
        bind_links(headline_tally, formatted_list)


#shows next 10 articles (if possible)
def next_button_function(formatted_list):
    global headline_tally
    if len(formatted_list) >= (headline_tally + 20):
        print(headline_tally)
        headline_tally += 10
        set_titles(headline_tally, formatted_list)
        bind_links(headline_tally, formatted_list)


#Getting the News, core of the program
#page 1 of news, requests articles from first page
res = requests.get("https://news.ycombinator.com/news")
soup = BeautifulSoup(res.text, "html.parser")
links = soup.select(".storylink")
subtext = soup.select(".subtext")

#page 2 of news
res = requests.get("https://news.ycombinator.com/news?p=2")
soup = BeautifulSoup(res.text, "html.parser")
links += soup.select(".storylink")
subtext += soup.select(".subtext")

#page 3 of news
res = requests.get("https://news.ycombinator.com/news?p=3")
soup = BeautifulSoup(res.text, "html.parser")
links += soup.select(".storylink")
subtext += soup.select(".subtext")

#Formatted list of articles and links
#Saves formatted list into a variable for ease of access
formatted_list = format_titles(sort_by_points(alternative_hacker_news(links, subtext)))
print(len(formatted_list))

#BEGIN TKINTER MAINLOOP
root = tk.Tk()

#default window size
default_window = tk.Canvas(root, height=900, width=800)
default_window.pack()

#background
bg = tk.Label(root, bg="black", bd=15)
bg.place(relwidth=1, relheight=1)

#Set icon and title for window
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./icon.ico'))
root.title("Hacker News Scraper")

#Make Title Label with link to hacker news
title_frame = tk.Frame(root)
title_frame.place(relx=0.2, rely=0.01, relwidth=0.6, relheight=0.1)

title_background = tk.Label(title_frame, bg="gray")
title_background.place(relwidth=1, relheight=1)

title_label = tk.Label(title_frame, bg="gray", text="Hacker News Parser Display", font=("Helvetica", 18, "bold"))
title_label.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.7)

hacker_news_link = tk.Label(title_frame, bg="gray", text="Click here to go to the original Hacker News website (source)", font=("Helvetica", 10, "underline"), cursor=title_cursor)
hacker_news_link.place(relx=0.025, rely=0.75, relheight=0.25, relwidth=0.95)
hacker_news_link.bind("<Button-1>", lambda e: open_url("https://news.ycombinator.com/"))

#FRAMES
#make frames
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame4 = tk.Frame(root)
frame5 = tk.Frame(root)
frame6 = tk.Frame(root)
frame7 = tk.Frame(root)
frame8 = tk.Frame(root)
frame9 = tk.Frame(root)
frame10 = tk.Frame(root)
#place the frames
frame1.place(relx=0.025, rely=0.125, relwidth=0.45, relheight=0.15)
frame2.place(relx=0.025, rely=0.3, relwidth=0.45, relheight=0.15)
frame3.place(relx=0.025, rely=0.475, relwidth=0.45, relheight=0.15)
frame4.place(relx=0.025, rely=0.65, relwidth=0.45, relheight=0.15)
frame5.place(relx=0.025, rely=0.825, relwidth=0.45, relheight=0.15)
frame6.place(relx=0.525, rely=0.125, relwidth=0.45, relheight=0.15)
frame7.place(relx=0.525, rely=0.3, relwidth=0.45, relheight=0.15)
frame8.place(relx=0.525, rely=0.475, relwidth=0.45, relheight=0.15)
frame9.place(relx=0.525, rely=0.65, relwidth=0.45, relheight=0.15)
frame10.place(relx=0.525, rely=0.825, relwidth=0.45, relheight=0.15)
#frame backgrounds
bg1 = tk.Label(frame1, bg="gray")
bg1.place(relwidth=1, relheight=1)
bg2 = tk.Label(frame2, bg="gray")
bg2.place(relwidth=1, relheight=1)
bg3 = tk.Label(frame3, bg="gray")
bg3.place(relwidth=1, relheight=1)
bg4 = tk.Label(frame4, bg="gray")
bg4.place(relwidth=1, relheight=1)
bg5 = tk.Label(frame5, bg="gray")
bg5.place(relwidth=1, relheight=1)
bg6 = tk.Label(frame6, bg="gray")
bg6.place(relwidth=1, relheight=1)
bg7 = tk.Label(frame7, bg="gray")
bg7.place(relwidth=1, relheight=1)
bg8 = tk.Label(frame8, bg="gray")
bg8.place(relwidth=1, relheight=1)
bg9 = tk.Label(frame9, bg="gray")
bg9.place(relwidth=1, relheight=1)
bg10 = tk.Label(frame10, bg="gray")
bg10.place(relwidth=1, relheight=1)

#LABELS
#make title labels


title_label1 = tk.Label(frame1, bg="gray", font=title_font, cursor=title_cursor)
title_label1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label2 = tk.Label(frame2, bg="gray", font=title_font, cursor=title_cursor)
title_label2.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label3 = tk.Label(frame3, bg="gray", font=title_font, cursor=title_cursor)
title_label3.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label4 = tk.Label(frame4, bg="gray", font=title_font, cursor=title_cursor)
title_label4.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label5 = tk.Label(frame5, bg="gray", font=title_font, cursor=title_cursor)
title_label5.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label6 = tk.Label(frame6, bg="gray", font=title_font, cursor=title_cursor)
title_label6.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label7 = tk.Label(frame7, bg="gray", font=title_font, cursor=title_cursor)
title_label7.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label8 = tk.Label(frame8, bg="gray", font=title_font, cursor=title_cursor)
title_label8.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label9 = tk.Label(frame9, bg="gray", font=title_font, cursor=title_cursor)
title_label9.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label10 = tk.Label(frame10, bg="gray", font=title_font, cursor=title_cursor)
title_label10.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

#BUTTONS
#make next and previous buttons
next_button = ttk.Button(root, text="Next", command=lambda: next_button_function(formatted_list), cursor=title_cursor)
next_button.place(relx=0.875, rely=0.06, relwidth=0.1, relheight=0.05)

previous_button = ttk.Button(root, text="Previous", command=lambda: previous_button_function(formatted_list), cursor=title_cursor)
previous_button.place(relx=0.025, rely=0.06, relwidth=0.1, relheight=0.05)


#Startup, so first 10 titles are shown straight away
bind_links(headline_tally, formatted_list)
set_titles(headline_tally, formatted_list)


root.mainloop()