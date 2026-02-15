#Sudoku Program
from tkinter import *
from tkinter import messagebox, simpledialog
import random
import copy
import time

class Sudoku:
    def __init__(self):
        self.grid= [[0]*9 for i in range(9)]
        self.genfullsol()

    def possible(self, r,c,n):
        for i in range(9):
            if self.grid[r][i] == n: return False
            if self.grid[i][c] == n: return False

        br,bc= (r//3)*3, (c//3)*3
        for i in range(br, br+3):
            for j in range(bc, bc+3):
                if self.grid[i][j] == n: return False
        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i,j
        return None

    def solve(self):
        empty= self.find_empty()
        if not empty:
            return True
        r,c= empty
        ns= list(range(1,10))
        for n in ns:
            if self.possible(r,c,n):
                self.grid[r][c] = n
                if self.solve():
                    return True
                self.grid[r][c] = 0
        return False

    def genfullsol(self):
        self.solve()

    def genpuzzle(self, diff="Easy"):
        diff_map= {"Easy":25,"Medium":45,"Hard":55,"Expert":60}
        holes= diff_map.get(diff,45)
        puz= copy.deepcopy(self.grid)
        rem= holes
        while rem>0:
            r,c= random.randint(0,8), random.randint(0,8)
            if puz[r][c] != 0:
                puz[r][c] = 0
                rem -= 1
        return puz

class SudokuGUI:
    def __init__(self, sud):
        self.sud= sud
        self.sud.title("Sudoku Game")
        self.sud.geometry("1000x600")
        self.sud.config(bg="#ffb90f")

        Label(sud, text="SUDOKU: GAME OF NUMBERS", font=("arial",26,"bold"), bg= "#ffb90f", fg="#8b6508").pack(pady=5)

        self.game= Sudoku()
        self.sol= copy.deepcopy(self.game.grid)
        self.diffselect()
        self.puz= self.game.genpuzzle(self.diffv.get())
        self.cells= {}
        self.mistakes= 0
        self.points= 100
        self.stime= time.time()
        self.timerrun= True
        self.bframe= None

        self.createboard()
        self.createcontrols()
        self.updatetimer()

    def createboard(self):
        if self.bframe:
            self.bframe.destroy()
        self.bframe= Frame(self.sud)
        self.bframe.pack(pady=10)
        for r in range(9):
            for c in range(9):
                val= self.puz[r][c]
                entry= Entry(self.bframe, width=2, font=("arial",20), justify="center", relief="ridge")
                entry.grid(row=r, column=c, ipadx=10, ipady=5, padx=1, pady=1)

                if val != 0:
                    entry.insert(0,str(val))
                    entry.config(state="disabled", disabledforeground="black")
                else:
                    entry.bind("<KeyRelease>", lambda e, row=r, col=c: self.checkinp(e,row,col))

                if c%3==0:
                    entry.grid(padx=(3,1))
                if r%3==0:
                    entry.grid(pady=(3,1))
                self.cells[(r,c)]= entry        

    def diffselect(self):
        self.diffv= StringVar()
        self.diffv.set("Easy")

        frame= Frame(self.sud, bg="#ffb90f")
        frame.pack(pady=10)

        Label(frame, text="Difficulty: ", font=("Times New Roman",12), bg="#ffb90f").pack(side=LEFT, padx=5)
        diffmenu= OptionMenu(frame, self.diffv, "Easy", "Medium", "Hard", "Expert",command=self.change_diffselect)
        diffmenu.config(font=("Arial",12),width=10)
        diffmenu.pack(side=LEFT, padx=5)

    def change_diffselect(self,val):
        diff_map= {"Easy":25,"Medium":45,"Hard":55,"Expert":60}
        holes= diff_map[val]

        self.game= Sudoku()
        self.sol= copy.deepcopy(self.game.grid)
        self.puz= self.game.genpuzzle(holes)

        self.mistakes= 0
        self.points= 100
        self.stime= time.time()
        self.timerrun= True
        self.cells={}

        self.createboard()
        self.updatetimer()

    def createcontrols(self):
        self.infol= Label(self.sud, text="Points: 100\t\tMistakes: 0\t\tTime: 0s", font=("Arial",12))
        self.infol.pack(pady=10)

        bframe= Frame(self.sud)
        bframe.pack()

        Button(bframe, text="Hint", command=self.givehint, bg="#d1e7dd").grid(row=0,column=0,padx=10)
        Button(bframe, text="Restart", command=self.restartg, bg="#f8d7da").grid(row=0,column=1,padx=10)

    def updatetimer(self):
        if self.timerrun:
            elp= int(time.time() - self.stime)
            self.infol.config(text=f"Points: {self.points}\t\tMistakes: {self.mistakes}\t\tTime: {elp}s")
            self.sud.after(1000, self.updatetimer)

    def checkinp(self, event, r,c):
        entry= self.cells[(r,c)]
        val= entry.get()

        if val=="":
            return
        if not val.isdigit() or not (1<=int(val)<=9):
            entry.delete(0,END)
            return

        num= int(val)
        if num == self.sol[r][c]:
            entry.config(fg="green", bg="#a0fda0", state="disabled")
            self.points += 50
        else:
            entry.delete(0,END)
            messagebox.showerror("Mistake","Incorrect Value! Try Again")
            entry.config(bg="#f8d7da")
            self.mistakes += 1
            self.points -= 10
        self.uptstatus()
        if self.checkwin():
            elp= int(time.time() - self.stime)
            self.timerrun= False
            messagebox.showinfo("Game Won!",f"Congratulations! You solved the Sudoku!\nTime: {elp}s\nMistakes: {self.mistakes}\nPoints: {self.points}")
            
    def uptstatus(self):
        elp= int(time.time() - self.stime)
        self.infol.config(text=f"Points: {self.points}\t\tMistakes: {self.mistakes}\t\tTime: {elp}s")

    def checkwin(self):
        for (r,c), entry in self.cells.items():
            if entry['state'] != 'disabled' or entry.get()=="":
                return False
        return True

    def givehint(self):
        empc= [(r,c) for (r,c), entry in self.cells.items() if entry['state'] != 'disabled' and entry.get()=='']
        if not empc:
            return
        r,c= random.choice(empc)
        self.cells[(r,c)].insert(0, str(self.sol[r][c]))
        self.cells[(r,c)].config(state="disabled", fg='blue')
        self.points -= 15
        self.uptstatus()

    def restartg(self):
        yn= messagebox.askyesno("Warning","Do you want to restart?")
        if yn:
            messagebox.showinfo("Restart Game","Restarting Game")
            self.sud.destroy()
            main()

def main():
    sud= Tk()
    SudokuGUI(sud)
    sud.mainloop()

if __name__ == "__main__":
    main()
