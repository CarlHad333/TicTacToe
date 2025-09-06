from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# from time import sleep
from tictactoe_root import TicTacToe



class Spot():
    def __init__(self):
        self.image

class XOApp():
    def __init__(self):
        #fenetre principale
        self.fenetre=Tk()
        self.fenetre.title("Tic-Tac-Toe")
        self.fenetre.minsize(500,500)
        self.fenetre.columnconfigure(0,weight=1)
        self.fenetre.configure(background="lightblue")
        self.stop=False
        
        
        ### Variables
        self.genres =["Human", "Random", "Minimax"]
        self.playerX = StringVar()
        self.playerO = StringVar()
        self.playerX.set("X")
        self.playerO.set("O")
        self.nameX = StringVar()
        self.nameO = StringVar()
        
        
        #frame du titre
        self.title_frame = ttk.Frame(self.fenetre, padding=20)
        self.title_frame.columnconfigure(0, weight=1)
        self.title_frame.grid(row=0, column=0, sticky="NSEW")
        
        self.titleLabel = ttk.Label(self.title_frame, text="Tic-Tac-Toe !...⚡❤",
                                    font=["Verdana", 20, "italic", "bold"], foreground="#ff0000")
        self.titleLabel.grid(sticky="N")
        self.titleLabel.bind("<Motion>", self.move)
        
        
        #frame des interactions prealables au jeu
        self.requests_frame = ttk.Frame(self.fenetre, padding=20)
        self.requests_frame.columnconfigure(0,weight=1)
        self.requests_frame.columnconfigure(1,weight=1)
        self.requests_frame.grid(row=1, column=0, sticky="NSEW")
        
        self.requestX_frame =self.requestPlayerLayout(self.requests_frame, self.playerX, self.nameX)
        self.requestO_frame =self.requestPlayerLayout(self.requests_frame, self.playerO, self.nameO)
        
        self.requestX_frame.grid(row=0, column=0)
        self.requestO_frame.grid(row=0, column=1)
        
        ttk.Button(self.requests_frame, text="Let the game begin!",
                   command=self.startGameSignal).grid(row=1, column=0, columnspan=2, pady=40)

        #frame de la grille
        self.board_frame = ttk.Frame(self.fenetre, padding=20)
        
        
        def on_closing():
            self.stop=True
            MsgBox = messagebox.askquestion('Exit Application','Are you sure you want to exit the application?',icon='warning')
            if MsgBox == 'yes':
                self.fenetre.destroy()
        self.fenetre.protocol("WM_DELETE_WINDOW", on_closing)
        self.fenetre.mainloop()
        
    def move(self, event, frame_period=25, extension_limit=25, jump_speed=3):
        self.titleLabel.unbind("<Motion>")
        i=extension_limit
        j=0
        l=[]
        #mem=self.titleLabel['font']
        def move_right(j):
            j+=jump_speed
            self.titleLabel.grid(padx=(i+j,i-j))
            #self.titleLabel['font']=["Verdana", 20+abs(j*5//extension_limit), "italic", "bold"]
            self.fenetre.update()
            return j
        def move_left(j):
            j-=jump_speed
            self.titleLabel.grid(padx=(i+j,i-j))
            #self.titleLabel['font']=["Verdana", 20+abs(j*5//extension_limit), "italic", "bold"]
            self.fenetre.update()
            return j
        while not self.stop and j<=i-jump_speed:
            self.fenetre.after(frame_period, l.append(move_right(j)))
            j=l.pop()
        while not self.stop and j>=-i+jump_speed:
            self.fenetre.after(frame_period, l.append(move_left(j)))
            j=l.pop()
        while not self.stop and j<=-jump_speed:
            self.fenetre.after(frame_period, l.append(move_right(j)))
            j=l.pop()
        if not self.stop:
            self.titleLabel.grid(padx=(0,0))
            #self.titleLabel['font']=mem
            self.fenetre.update()
            self.titleLabel.bind("<Motion>", self.move)    
            
    def requestPlayerLayout(self, parent_container, player_var, player_name):
        frame = ttk.Frame(parent_container, padding=5)
        ttk.Label(frame, style="Request.TLabel",
                  text="Who is player {} ?".format(player_var.get())).grid(row=0, column=0)
        player_var.set("Human")
        playerSet = ttk.Combobox(frame, values=self.genres, state="readonly", textvariable=player_var, width=20)
        playerSet.grid(row=1, column=0, pady=5)
        ttk.Label(frame, style="Request.TLabel",
                  text="Enter a name (optional) :").grid(row=2, column=0, sticky=W, pady=(10,5))
        ttk.Entry(frame, textvariable=player_name, width=25).grid(row=3, column=0)
        return frame
    
    def startGameSignal(self):
        self.requests_frame.grid_forget()
        self.TTT = TicTacToe()
        self.TTT.setPlayers(self.playerX.get()[0], self.playerO.get()[0])
        self.board_frame.grid(row=1, column=0)
        
if __name__ == '__main__':
    XOApp()
