import numpy as np 
import cv2

class KalmanFilter(object): 
    """dt : temps d'actualisation 
    point : coordonné initiaux du point
    erreur : plus l'entier est grand, plus le filtre pense que c'est brouillé """
    def __init__ (self, dt, point, erreur):
        self.dt = dt
        self.erreur = int(erreur)

        #vecteur 
        self.E=np.matrix([[point[0]],[point[1]], [0],[0]])

        #Matrice de transition 
        self.A=np.matrix([[1, 0, self.dt, 0],
                          [0, 1, 0, self.dt],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
        
           # Matrice d'observation, on observe que x et y
        self.H=np.matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0]])

        self.Q=np.matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        self.R=np.matrix([[erreur, 0],
                          [0, erreur]])

        self.P=np.eye(self.A.shape[1])

    def predict(self):
        self.E=np.dot(self.A, self.E)
        # Calcul de la covariance de l'erreur
        self.P=np.dot(np.dot(self.A, self.P), self.A.T)+self.Q
        return self.E

    def update(self, z):
        # Calcul du gain de Kalman
        S=np.dot(self.H, np.dot(self.P, self.H.T))+self.R
        K=np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # Correction / innovation
        self.E=np.round(self.E+np.dot(K, (z-np.dot(self.H, self.E))))
        I=np.eye(self.H.shape[1])
        self.P=(I-(K*self.H))*self.P

        return self.E
class Annexe(object):
    def __init__(self,w,h,mw,mh):
        self.width = w
        self.height = h
        self.mid_w = mw
        self.mid_h = mh       

    def scored(self, x,y,x2,y2,x3,y3): 
        if x <x3 and x3 <x2 and y< y2 and y2< y3 :
            return True
        else :
            return False 
        

    def detect_ball(self, image, min_surface,max_surface,lo,hi):
        """Renvoie un tableau trié par surface décroissante"""
        points=np.empty(2,int)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image=cv2.blur(image, (10, 10))
        mask=cv2.inRange(image, lo, hi)
        mask=cv2.erode(mask, None, iterations=4)
        mask=cv2.dilate(mask, None, iterations=4)
        elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        elements=sorted(elements, key=lambda x:cv2.contourArea(x), reverse=True)
        for element in elements:
            if cv2.contourArea(element)>min_surface and cv2.contourArea(element)<max_surface:
                ((x, y), _)=cv2.minEnclosingCircle(element)
                points =np.append(points,np.array([int(x), int(y)]))
            else:
                break
        return points,mask 
    

    def detect_bu(self, frame,min_surface,lo,hi): 
        """Renvoie un tableau trié par surface décroissante"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        image=cv2.blur(hsv, (10, 10))
        bu_mask=cv2.inRange(image, lo, hi)
        bu_mask=cv2.erode(bu_mask, None, iterations=4)
        bu_mask=cv2.dilate(bu_mask, None, iterations=4)
        contours_bu=cv2.findContours(bu_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours_bu=sorted(contours_bu, key=lambda x:cv2.contourArea(x), reverse=True)
        bu_count = 0 
        for countour in contours_bu : 
            area_bu = cv2.contourArea(countour)
            xb,yb,wb,hb = cv2.boundingRect(countour)
            if area_bu > min_surface and  yb < self.height and 2*self.mid_w<xb < self.width :
                cv2.rectangle(image, (xb,yb),(xb+wb,yb+hb), (255,255,255),2)
                bu_count += 1
        return bu_count, bu_mask