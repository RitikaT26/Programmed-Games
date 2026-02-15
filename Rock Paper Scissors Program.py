#Rock Paper Scissors Program
from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk

choices= ['Rock','Paper','Scissors']

uc, cc, tc = 0,0,0

def decidewin(userc, compc):
    if userc == compc:
        return "It is a Tie!"
    elif (userc=='Rock' and compc=='Scissors') or \
    (userc=='Scissors' and compc=='Paper') or \
    (userc=='Paper' and compc=='Rock'):
        return "You Win!"
    else:
        return "You Lose!"

def playgame(choice):
    global choices, uc, cc, tc
    compc= random.choice(choices)
    userlc.config(text= f"Your Choice: {choice}")
    complc.config(text= f"Computer's Choice: {compc}")

    result= decidewin(choice,compc)
    if result=="You Win!":
        uc += 1
        messagebox.showinfo("Information","User Wins!")
        pu.config(text="User: Winner ↑")
        pc.config(text="Computer: Loser ↓")
    elif result== "You Lose!":
        cc += 1
        messagebox.showinfo("Information","Computer Wins!")
        pu.config(text="User: Loser ↓")
        pc.config(text="Computer: Winner ↑")
    else:
        tc += 1
        messagebox.showinfo("Information","It is a Tie!")
        pu.config(text="Tie")
        pc.config(text="Tie")
    #resultlc.config(text= result)
    updatesc()

def updatesc():
    score.config(text= f"User: {uc} Computer: {cc} Ties: {tc}")

def exit():
    msg= messagebox.askyesno("Exit Game","Are you sure to exit the game?")
    if msg:
        messagebox.showinfo("Thank You!","Thank You!")
        rps.destroy()

rps= Tk()
rps.title("Rock Paper Scissors")
rps.geometry("450x450")
rps.resizable(False,False)
rps.config(background="#ffc281")

Label(rps, text="Rock Paper Scissors".upper(), font=("Times New Roman", 20, "bold"), fg="#ff8503").pack(fill=X, pady=10)
pu= Label(rps, text="", font=("Times New Roman",14), fg='#191209', bg="#ffc281")
pu.pack()
userlc= Label(rps, text="Your Choice: None", font=("Times New Roman",14), fg='#191209', bg="#ffc281")
userlc.pack()
Label(rps, text='VS', font=("Times New Roman",14), bg="#ffc281").pack()
complc= Label(rps, text="Computer's Choice: None", font=("Times New Roman",14), fg='#191209', bg="#ffc281")
complc.pack()
pc= Label(rps, text="", font=("Times New Roman",14), fg='#191209', bg="#ffc281")
pc.pack()
score= Label(rps, text="User: 0 Computer: 0 Ties: 0", font=("Times New Roman",14), bg="#ffc281")
score.pack(pady=5)

rockimg= ImageTk.PhotoImage(Image.open("rock.png").resize((100,100)))
paperimg= ImageTk.PhotoImage(Image.open("paper.png").resize((100,100)))
scissorsimg= ImageTk.PhotoImage(Image.open("scissors.png").resize((100,100)))

rpsframe= Frame(rps)
rpsframe.pack(pady=10)

rb= Button(rpsframe, image=rockimg, command= lambda: playgame("Rock"))
rb.grid(row=0,column=0)
pb= Button(rpsframe, image=paperimg, command= lambda: playgame("Paper"))
pb.grid(row=0,column=1)
sb= Button(rpsframe, image=scissorsimg, command= lambda: playgame("Scissors"))
sb.grid(row=0,column=2)

Button(rps, text="Exit", width=15, command= exit).pack(pady=10)

rps.mainloop()
