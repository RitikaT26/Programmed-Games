#Tic Tac Toe Program
from tkinter import *
from tkinter import messagebox

ttt= Tk()
ttt.geometry('400x370')
ttt.title('Tic tac Toe')
ttt.config(background= '#5c1839')
ttt.resizable(False,False)

head= Label(ttt, text='TIC TAC TOE', font=('Times New Roman', 24, 'bold'), fg='#87285f')
head.grid(row=0,column=0, columnspan=10, sticky='nsew', pady=15)

boardf= Frame(ttt, bg= '#9f527e', padx=5, pady=5)
boardf.grid(row=1, column=0, padx=10, pady=10)

#score card
sx, so= 0,0
scoref= Frame(ttt)
scoref.grid(row=1,column=1, pady=(0,10))

Label(scoref, text='Player X', font= ('Times New Roman', 16, 'bold'), fg='#920dff', width=10).grid(row=0,column=0, padx=5)
Label(scoref, text='Player O', font= ('Times New Roman', 16, 'bold'), fg='#f20c00', width=10).grid(row=2,column=0, padx=5)

sxl= Label(scoref, text=str(sx), font= ('Times New Roman', 16), fg='#920dff', width=10)
sxl.grid(row=1,column=0, padx=5)
sol= Label(scoref, text=str(so), font= ('Times New Roman', 16), fg='#f20c00', width=10)
sol.grid(row=3,column=0, padx=5)

cplay= 'X'
buttons= [[None for i in range(3)] for i in range(3)]

def updatescore():
    sxl.config(text= str(sx))
    sol.config(text= str(so))
    
def checkwin():
    #row-wise match
    for r in range(3):
        if buttons[r][0]['text'] == buttons[r][1]['text'] == buttons[r][2]['text'] != '':
            showwin([(r,0),(r,1),(r,2)])
            return True
    #column-wise match
    for c in range(3):
        if buttons[0][c]['text'] == buttons[1][c]['text'] == buttons[2][c]['text'] != '':
            showwin([(0,c),(1,c),(2,c)])
            return True
    #diagonal-wise match
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        showwin([(0,0),(1,1),(2,2)])
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        showwin([(0,2),(1,1),(2,0)])
        return True

def showwin(cells):
    for r,c in cells:
        buttons[r][c].config(bg='#39ff14')

def checktie():
    return all(buttons[r][c]['text'] != '' for r in range(3) for c in range(3))

def click(r,c):
    global cplay, sx, so
    if buttons[r][c]['text'] == '':
       if cplay == 'X':
          buttons[r][c].config(text='✕', fg='#920dff', font=(16,))
       else:
          buttons[r][c].config(text='◯', fg='#f20c00', font=(16,))

       if checkwin():
          if cplay == 'X':
              sx += 1
          else:
              so += 1
          updatescore()
          messagebox.showinfo('Game Over!', f'Player {cplay} wins!')
          resetgame()
       elif checktie():
          messagebox.showinfo('Game Over', 'It is a Tie!')
          resetgame()
       else:
          cplay= 'O' if cplay=='X' else 'X'

def fullreset():
    global sx,so
    sx=0
    so=0
    updatescore()
    resetgame()
    messagebox.showinfo('Reset Game', 'Score Reset')

def resetgame():
    global cplay
    cplay='X'
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text='', fg='black', bg='SystemButtonFace')

for r in range(3):
    for c in range(3):
        b= Button(boardf, text='', width=5, height=2, font=('Times New Roman', '16', 'bold'), command= lambda r=r, c=c: click(r,c))
        b.grid(row=r, column=c, padx=3, pady=3)
        buttons[r][c]=b

resetb= Button(ttt, text='Reset Game', font=('Times New Roman',14), command= fullreset)
resetb.grid(row=2, column=0, pady=10)
ttt.mainloop()
