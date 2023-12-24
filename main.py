from PIL import Image, ImageGrab
import pytesseract
import cutlet
import os, time
import translators as ts
import translators.server as tss
import wx

class Translator():

    def getLines(self, x1, y1, x2, y2):
        bbox = (x1,y1,x2,y2)

        im = ImageGrab.grab(bbox)
        # print('languages:' + pytesseract.get_languages())

        text_raw = pytesseract.image_to_string(im, lang='eng', config='--psm 11')
        text = text_raw.replace('/', '!')

        #Borrar espacios en blanco
        text = '\n'.join([ line.rstrip() for line in text.splitlines() if line.strip() ])
        lines = text.splitlines()
        return lines

    def startReading(self, x1, y1, x2, y2):
        # katsu = cutlet.Cutlet()
        # katsu.use_foreign_spelling = False

        lines = ''

        while True:

            new_lines = self.getLines(x1, y1, x2, y2)

            if lines != new_lines:
                os.system('clear')
                lines = new_lines

                for line in lines:
                    print(line)
                    # print(katsu.romaji(line))
                    print(ts.translate_text(line, to_language='es'))
                    print('-----------------------------')

            time.sleep(0.1)



class DesktopController(wx.Frame):
    def __init__(self, parent, title):
        super( DesktopController, self ).__init__(parent, title=title)

        self.SetTransparent(255)
        self.button = wx.Button(self)

        self.Bind(wx.EVT_BUTTON, self.onButtonClick, self.button)

        self.SetPosition(wx.Point(0,0))
        self.Show()

    def onButtonClick(self, event):
        
        size = self.button.Size
        x1,y1 = self.button.GetScreenPosition()
        x2,y2 = x1 + size[0], y1 + size[1]
        self.Hide()

        Translator().startReading(x1, y1, x2, y2)



if __name__ == '__main__':
    app = wx.App()

    mainFrame = DesktopController(None, title='Select an area')
    app.MainLoop()