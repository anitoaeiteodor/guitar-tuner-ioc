import cv2
import threading
from PySide6 import QtGui
import os

class EyeTracker:
    def __init__(self) -> None:
        self._run_flag = False
        # self.runningThread = threading.Thread(target=self.runLoop)

    def start(self):
        self._run_flag = True
        self.runLoop()

    def stop(self):
        self._run_flag = False

    def runLoop(self):
        # construire stream video
        print('Starting')
        cascpath = os.path.dirname(cv2.__file__) + '/data/haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascpath)
        videoStream = cv2.VideoCapture(0)
        while self._run_flag:
            # preluare imagine
            ret, cvImg = videoStream.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if ret:
                # flip horizontal imagine
                cvImg = cv2.flip(cvImg,1)
                # conversie gray scale
                gray = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
                # detecție caracteristici
                faceRects = face_cascade.detectMultiScale(gray, 1.3, 5)
                # intr-o imagine pot fi mai multe fețe (caracteristici cautate)
                for (x, y, w, h) in faceRects:
                    # desenare unui punct in centrul dreptunghiului ce incadreaza caracteristicile
                    # detectate (fata/ochii)
                    # coordonatele punctului sunt: x + int(w / 2), y + int(h / 2)
                    xc = x + int(w / 2)
                    yc = y + int(h / 2)

                    tx = x - xc
                    ty = y - yc

                    cv2.rectangle(cvImg, (xc, yc), (xc, yc), (0, 255, 0), 3)
                    # cv2.imshow('face', cvImg)
                    # ecuație de transformare fereastra poarta
                    xt = x * 1 + tx
                    yt = y * 1 + 200 * 1

                    cv2.rectangle(cvImg, (xt, yt), (xt, yt), (255, 0, 0), 3)
                    cv2.imshow('eye', cvImg)


                    # snap to grid
                    # avand in vedere ca mouse-ul nu va sta fix pe ecran, se va adauga un filtru
                    # suplimentar ce va consta intr-un grid avand cate un punct in centrul
                    # elementului activ de pe interfața (buton, meniu etc) orice coordonate (xt,yt)
                    # aflate in aria unui element activ vor fi modificate astfel incat sa preia
                    # coordonatele centrului elementului respectiv

                    # xg = gx(xt)
                    # yg = gy(yt)
                    
                    # QtGui.QCursor.setPos(xg, yg)
                    # daca cursorul este ținut in aria respectivă un timp de 2 secunde generați un
                    # eveniment click stanga
                
                    # if time > 2sec:
                    #     pyautogui.leftClick()

                    # actualizare imagine pe interfața
                    # self.change_pixmap_signal.emit(cv_img)



        videoStream.release()
        # Destroy all the windows
        cv2.destroyAllWindows()


if __name__ == '__main__':
    eyeTracker = EyeTracker()
    eyeTracker.start()