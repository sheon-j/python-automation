from tkinter import filedialog
from tkinter import *
import crawler
import tkinter

def app():
    window=Tk()

    window.title("베스킨라빈슨 크롤링 프로그램")
    window.geometry("640x400+100+100")
    window.resizable(False, False)
    window.dirName = '.'

    label=tkinter.Label(window, text='''

███▌▓▓▓▓▓───▓▓▓▐███▄──
███▌───▓▓▓──▓▓▓──▀███─
███▌────▓▓▓─▓▓▓────▀██
███▌───▓▓▓──▓▓▓───▄██─
███▌▓▓▓▓▓───▓▓▓▐███▀──
─██▌───▓▓▓───▓▓▐█▄────
─██▌────▓▓───▓▓──██───
──█▌▓▓▓▓▓─────▓───▀█──
\n베스킨 라빈스 이달의 맛 유튜브 반응 조사\n\n''')
    label.pack()

    #저장폴더위치 선택
    def ask():
        window.dirName = filedialog.askdirectory()
        txt.configure(text="폴더 위치: " + window.dirName)
        print (window.dirName)

    def getTextInput():
        result = textExample.get("1.0","end")
        crawler.crawler(result, window.dirName)
        print(result)

    txt = tkinter.Label(window, text="\n폴더 위치")
    txt.pack()
    txt.place()

    button = tkinter.Button(window, text="저장 폴더 위치", overrelief="solid", width=10, command=ask)
    button.pack()
    button.place(x=0, y=200, relx=0.405)
        
    textExample=tkinter.Text(window, height=1)
    textExample.pack()
    textExample.place(x=40, y=300)

    label2=tkinter.Label(window, text="입력 예시: 베스킨라빈스 오레오 쿠키앤 스트로베리")
    label2.pack()
    label2.place(x=200,y=270)

    btnRead=tkinter.Button(window, height=1, width=10, text="크롤링 시작", command=getTextInput)
    btnRead.pack()
    btnRead.place(x=0, y=350, relx=0.405)

    window.mainloop()

if __name__ == '__main__' :
    app()
