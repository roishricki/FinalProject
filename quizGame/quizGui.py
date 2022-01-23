import os
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import recWav
import stt_class
import tts_ref
import sounddevice as sd
import soundfile as sf


def recordAudio():
    recWav.record()
    wordAndConfidence= procces()
    index = levellbl.cget("text")
    print(index)
    print(englishWords[(int(index))-1])
    try:
        if isSameWord(wordAndConfidence[0],englishWords[(int(index))-1]):
            feedbacklbl=Label(
            text="!תשובה נכונה\n נאמר ב{}% באופן נכון".format((int(wordAndConfidence[1]*100))),
            font=("Arial", 17, "bold"),
            background="#ffffff",
            fg="#4aac00"
            )
            feedbacklbl.grid(row=4,column=1,pady=(0,20))
            feedbacklbl.after(2500, lambda: feedbacklbl.destroy())
            btnRecord.grid_forget()
            btnNextHebWord.grid(row=5, column=1, pady=(0, 0))
            scoreLabel.configure(text="{} : ניקוד".format(score.pop(0)))
        else:
            feedbacklbl = Label(
                text="!תשובה שגויה\n"
                     "{} :המילה שלך\n"
                     "{} :המילה הנכונה\n".format(wordAndConfidence[0], englishWords[(int(index)) - 1]),
                font=("Arial", 17, "bold"),
                background="#ffffff",
                fg="#ff0000"
            )
            feedbacklbl.grid(row=4, column=1, pady=(0, 20))
            feedbacklbl.after(2000, lambda: feedbacklbl.destroy())
            btnRecord.grid_forget()
            output = str.format("")
            print("didn't match\n your word is {}\ngame word is {}".format(wordAndConfidence[0],englishWords[(int(index))-1]))
    except :
        feedbacllbl = Label(
            text="נסה להקליט שוב בבקשה\n",
            font=("Arial", 17, "bold"),
            background="#ffffff",
            fg="#ff0000"
        )
        feedbacllbl.grid(row=4, column=1, pady=(0, 20))
        feedbacllbl.after(2000, lambda: feedbacllbl.destroy())

def tts_Function():
    index= (int)(levellbl.cget("text"))
    wavFileName=englishSoundWords[index-1]+".wav"
    AMP = 2
    data, fs = sf.read(wavFileName, dtype='float32')
    print('Starting playing')
    sd.play(data * AMP, fs)
    status = sd.wait()  # Wait until file is done playing
    print('Stop playing')


def procces():
    st = stt_class.STT()
    audio = st.opensoundfile("output.wav")
    rz = st.recognize(audio)
    for result in rz.results:
        wordAndConfidence = []
        wordAndConfidence.append(result.alternatives[0].transcript)
        wordAndConfidence.append(result.alternatives[0].confidence)
        return wordAndConfidence

def isSameWord(wordA,wordB):
    if wordA == wordB:
        return True
    else:
        return False


def toMainPage():
    labelImage.grid(row=1, column=1)
    labelText.grid(row=2, column=1)
    btnHebToEng.grid(row=3, column=1, pady=(10, 0))
    btnEngToEng.grid(row=4, column=1, pady=(10, 0))
    btnRules.grid(row=5, column=1,pady=(20,0))

def toGameHebToEngPage():
    levellbl.grid(row=2,column=1,pady=(50,0))
    wordlbl.grid(row=3,column=1,pady=(50,0))
    frameLabelImage.grid(row=3,column=1,pady=(50,0))
    btnRecord.grid(row=4,column=1,pady=(0,20))
    scoreLabel.grid(row=6,column=1,pady=(0,0))
    btnBackFromHebGame.grid(row=7,column=1,pady=(20,0))

def toGameEngToEng():
    levellbl.grid(row=1,column=1,pady=(50,0))
    tapHereToSoundLabelImage.grid(row=3,column=1,pady=(50,0))
    word_label.grid(row=4,column=1,pady=(50,0))
    word_entry.grid(row=5,column=1)
    btnSubmit.grid(row=6,column=1,pady=(5,0))
    scoreLabel.grid(row=7,column=1,pady=(100,0))
    btnBackFromEngGame.grid(row=9,column=1,pady=(20,0))

def backFromEngGame_is_pressed():
    levellbl.grid_forget()
    tapHereToSoundLabelImage.grid_forget()
    word_label.grid_forget()
    word_entry.grid_forget()
    btnSubmit.grid_forget()
    scoreLabel.grid_forget()
    btnBackFromEngGame.grid_forget()
    btnNextEngWord.grid_forget()
    reset_Game()
    scoreLabel.configure(text="{} : ניקוד".format(score.pop(0)))
    levellbl.configure(text="{}".format(levels.pop(0)))
    toMainPage()

def submitText():
    submitedWord=word_var.get()
    checkIfAnswerRight(submitedWord)
    word_var.set("")

def checkIfAnswerRight(word):
    index= (int)(levellbl.cget("text"))
    btnBackFromEngGame.grid_forget()
    btnBackFromEngGame.after(2000,lambda :btnBackFromEngGame.grid(row=9,column=1,pady=(20,0)))
    if word == englishSoundWords[index-1]:
        answerLabel=Label(
            text=word,
            font=("Arial",70,"bold"),
            background="#ffffff",
            fg="#4aac00"
        )
        feedbacllbl = Label(
            text="תשובה נכונה!\n",
            font=("Arial", 23, "bold"),
            background="#ffffff",
            fg="#4aac00"
        )
        answerLabel.grid(row=2,column=1)
        answerLabel.after(2000,lambda :answerLabel.destroy())
        feedbacllbl.grid(row=7, column=1, pady=(0,10))
        feedbacllbl.after(2000, lambda: feedbacllbl.destroy())
        word_entry.grid_forget()
        word_label.grid_forget()
        btnSubmit.grid_forget()
        btnNextEngWord.after(2000,lambda : btnNextEngWord.grid(row=8, column=1, pady=(50, 0)))
        scoreLabel.configure(text="{} : ניקוד".format(score.pop(0)))
    else:
        btnBackFromEngGame.grid_forget()
        answerLabel = Label(
            text="{} : התשובה שלך\n{} : התשובה הנכונה".format(word,englishSoundWords[index-1]),
            font=("Arial", 50, "bold"),
            background="#ffffff",
            fg="#ff0000"
        )
        gameoverlbl=Label(
            text="GAME OVER",
            font=("Arial", 70, "bold"),
            background="#ffffff",
            fg="#ff0000"
        )
        word_entry.grid_forget()
        word_label.grid_forget()
        btnSubmit.grid_forget()
        scoreLabel.grid_forget()
        scoreLabel.grid(row=7, column=1, pady=(20, 0))
        tapHereToSoundLabelImage.grid_forget()
        gameoverlbl.grid(row=7,column=1,pady=(50,50))
        answerLabel.grid(row=2,column=1)
        answerLabel.after(3000,lambda :answerLabel.destroy())
        gameoverlbl.after(3000,lambda :gameoverlbl.destroy())
        btnBackFromEngGame.after(3000,lambda :btnBackFromEngGame.grid(row=9,column=1,pady=(20,0)))


def nextWordHeb_is_pressed():
    if  hebWords[0] == "DONE" :
        print("stop")
    else:
        btnRecord.grid(row=4, column=1, pady=(0, 20))
        btnNextHebWord.grid_forget()
        hebWords.append(hebWords[0])
        wordlbl.configure(text=hebWords.pop(0))
        print(wordlbl.cget("text"))
        levellbl.configure(text="{}".format(levels.pop(0)))

def nextWordEng_is_pressed():
    if levellbl.cget("text")=="10":
        print("stop")
        btnNextEngWord.grid_forget()
    else:
        btnNextEngWord.grid_forget()
        levellbl.configure(text="{}".format(levels.pop(0)))
        word_label.grid(row=4, column=1, pady=(50, 0))
        word_entry.grid(row=5, column=1)
        btnSubmit.grid(row=6, column=1, pady=(5, 0))

def toRulesPage():
    labelRulesImage.grid(pady=(0, 0))
    lblRules.grid(pady=(80, 0))
    btnBackFromRules.grid(pady=(20, 0))

def rules_is_pressed():
    labelImage.grid_forget()
    labelText.grid_forget()
    btnHebToEng.grid_forget()
    btnEngToEng.grid_forget()
    btnRules.grid_forget()
    toRulesPage()

def backFromHebGame_is_pressed():
    btnBackFromHebGame.grid_forget()
    btnNextHebWord.grid_forget()
    wordlbl.grid_forget()
    levellbl.grid_forget()
    frameLabelImage.grid_forget()
    scoreLabel.grid_forget()
    btnRecord.grid_forget()
    reset_Game()
    resetHebrewWords()
    scoreLabel.configure(text="{} : ניקוד".format(score.pop(0)))
    wordlbl.configure(text=hebWords.pop(0))
    levellbl.configure(text="{}".format(levels.pop(0)))
    toMainPage()




def backFromRules_is_pressed():
    labelRulesImage.grid_forget()
    lblRules.grid_forget()
    btnBackFromRules.grid_forget()
    toMainPage()



def hebToEng_is_pressed():
    labelImage.grid_forget()
    labelText.grid_forget()
    btnHebToEng.grid_forget()
    btnEngToEng.grid_forget()
    btnRules.grid_forget()
    toGameHebToEngPage()

def engToEng_is_pressed():
    labelImage.grid_forget()
    labelText.grid_forget()
    btnHebToEng.grid_forget()
    btnEngToEng.grid_forget()
    btnRules.grid_forget()
    toGameEngToEng()


root = tkinter.Tk()
root.title("Speech Translator")
root.geometry("1250x860")
root.config(background="#ffffff")

englishSoundWords=["Melon","Coconut","Table","Sun","Bicycle","Sky","Street","Button","Knife","Complicated"]
tts_ref.toSound(englishSoundWords)

img = ImageTk.PhotoImage(Image.open("MainIMG.png"))
labelImage = Label(
    root,
    image=img,
    background="#ffffff"
)
# labelImage.pack(pady=0)
labelImage.grid(row=1, column=1)

labelText = Label(
    root,
    text="ברוכים הבאים\n"
         "משחק לשיפור האנגלית\n",
    font=("Arial", 28, "bold"),
    background="#ffffff"
)

# labelText.pack()
labelText.grid(row=2, column=1)

hebToEngImg = ImageTk.PhotoImage(Image.open("HebToEngBTN.png"))
engToEngImg = ImageTk.PhotoImage(Image.open("EngToEngBTN.png"))

btnEngToEng = Button(
    root,
    image=engToEngImg,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=engToEng_is_pressed,
)


btnHebToEng = Button(
    root,
    image=hebToEngImg,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=hebToEng_is_pressed,
)

btnHebToEng.grid(row=3, column=1,pady=(10,0))
btnEngToEng.grid(row=4,column=1,pady=(10,0))


rulesImg = ImageTk.PhotoImage(Image.open("RulesButton.png"))
frameWordIMG = ImageTk.PhotoImage(Image.open("FrameWord1.png"))
frameLabelImage = Label(
    root,
    image=frameWordIMG,
    background="#ffffff"
)
tapHereToSoundIMG=ImageTk.PhotoImage(Image.open("tapHereToSoundBTN.png"))
tapHereToSoundLabelImage = Button(
    root,
    image=tapHereToSoundIMG,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=tts_Function,
)

btnRules = Button(
    root,
    image=rulesImg,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=rules_is_pressed,

)
btnRules.grid(row=5, column=1, pady=(20, 0))
rulesLogoImg = ImageTk.PhotoImage(Image.open("RulesIMG.png"))

labelRulesImage = Label(
    root,
    image=rulesLogoImg,
    background="#ffffff"
)

backButtonImg = ImageTk.PhotoImage(Image.open("BackFromEng.png"))

btnBackFromRules = Button(
    root,
    image=backButtonImg,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=backFromRules_is_pressed,
)
btnBackFromEngGame = Button(
    root,
    image=backButtonImg,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=backFromEngGame_is_pressed,
)

btnBackFromHebGame = Button(
    root,
    image=backButtonImg,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=backFromHebGame_is_pressed,
)


lblRules = Label(
    root,
    text="כל משחק מכיל עשר שאלות\n\n"
         "המטרה : לבדוק ולשפר את רמת האנגלית שלך\n\n"
         ".המשחק עובד על שמיעה, כתיבה ודיבור באנגלית\n\n"
         ": קיימים שני סוגי משחקים\n\n"
         "קריאה בעברית -> דיבור באנגלית\n"
         "שמיעה באנגלית -> כתיבה באנגלית\n\n"
         " 100 : ניקוד עבור כל תשובה נכונה\n"
         "1000 : ניקוד מקסימלי\n",
         # "GOAL : Checking the level of confidence in saying English words\n"
         # "What Do You Need To Do? : You Get a Word In Hebrew, Then Have To Translate And Say It in English\n"
         # "You will receive a score for every question, ranging from A to F (A--> 100 , F--> Under 20)\n"
         # "If you Get an E or F Score - You Lose",
    width=100,
    font=("Arial", 23, "bold"),
    background="#ffffff"
)
btnRecordIMG = ImageTk.PhotoImage(Image.open("recordButton.png"))
btnRecord = Button(
    root,
    image=btnRecordIMG,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=recordAudio
)

btnSubmit = Button(
    root,
    text="שלח",
    font=("Arial", 20, "bold"),
    command=submitText
)

nextWordBtnIMG = ImageTk.PhotoImage(Image.open("nextWordButton.png"))

btnNextHebWord = Button(
    root,
    image=nextWordBtnIMG,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=nextWordHeb_is_pressed,
)
btnNextEngWord = Button(
    root,
    image=nextWordBtnIMG,
    relief=FLAT,
    background="#ffffff",
    border=0,
    command=nextWordEng_is_pressed,
)


def reset_Game():
    levels.clear()
    levels.append(1)
    levels.append(2)
    levels.append(3)
    levels.append(4)
    levels.append(5)
    levels.append(6)
    levels.append(7)
    levels.append(8)
    levels.append(9)
    levels.append(10)
    score.clear()
    score.append(0)
    score.append(100)
    score.append(300)
    score.append(400)
    score.append(500)
    score.append(600)
    score.append(700)
    score.append(800)
    score.append(900)
    score.append(1000)

def resetHebrewWords():
    hebWords.clear()
    hebWords.append("אופניים")
    hebWords.append("שָׁעוֹן")
    hebWords.append("מִקלֶדֶת")
    hebWords.append("אֵיכוּת")
    hebWords.append("מוּרכָּב")
    hebWords.append("הַמלָצָה")
    hebWords.append("הִתְפּוֹצְצוּת")
    hebWords.append("קָבוּעַ")
    hebWords.append("מַשְׁמָעוּת דוּ")
    hebWords.append("השלכות")
    hebWords.append("DONE")

hebWords = []
hebWords.append("אופניים")
hebWords.append("שָׁעוֹן")
hebWords.append("מִקלֶדֶת")
hebWords.append("אֵיכוּת")
hebWords.append("מוּרכָּב")
hebWords.append("הַמלָצָה")
hebWords.append("הִתְפּוֹצְצוּת")
hebWords.append("קָבוּעַ")
hebWords.append("מַשְׁמָעוּת דוּ")
hebWords.append("השלכות")
hebWords.append("DONE")

englishWords = []
englishWords.append("bicycle")
englishWords.append("clock")
englishWords.append("keyboard")
englishWords.append("quality")
englishWords.append("complex")
englishWords.append("recommendation")
englishWords.append("explosion")
englishWords.append("constant")
englishWords.append("ambiguity")
englishWords.append("consequences")

word_var=tkinter.StringVar()
word_label = tkinter.Label(root, text='הכנס את התשובה בתיבה', font=('Arial', 16, 'bold'),background="#ffffff")
word_entry = tkinter.Entry(root, textvariable=word_var, font=('calibre', 20, 'normal'),background="#d0d0d0")

levels =[1,2,3,4,5,6,7,8,9,10]
wordlbl= Label(
        root,
        text = "{}".format(hebWords.pop(0)),
        font=("Comic sans MS", 52, "bold"),
        background="#ffffff"
                   )

levellbl = Label(
    root,
    text="{}".format(levels.pop(0)),
    font=("Arial",36,"bold"),
    background="#ffffff"
)
score =[0,100,200,300,400,500,600,700,800,900,1000]
scoreLabel = Label(
    root,
    text="{} : ניקוד".format(score.pop(0)),
    font=("Comic sans MS", 36, "bold"),
    background="#ffffff"
)
root.grid_columnconfigure((0, 1, 2), weight=2)
root.mainloop()
