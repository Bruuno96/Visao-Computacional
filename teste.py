#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv
import math

import cv2
import os, sys, os.path
import numpy as np

# filtro baixo
image_lower_hsv1 = np.array([160, 130, 190])
image_upper_hsv1 = np.array([180, 205, 255])
# filtro alto
image_lower_hsv2 = np.array([0, 130, 190])
image_upper_hsv2 = np.array([10, 205, 255])


def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    """ retorna a imagem filtrada"""
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask


def mascara_or(mask1, mask2):
    """ retorna a mascara or"""
    mask = cv2.bitwise_or(mask1, mask2)
    return mask


def mascara_and(mask1, mask2):
    """ retorna a mascara and"""
    mask = cv2.bitwise_and(mask1, mask2)

    return mask


def desenha_cruz(img, cX, cY, size, color):
    """ faz a cruz no ponto cx cy"""
    cv2.line(img, (cX - size, cY), (cX + size, cY), color, 5)
    cv2.line(img, (cX, cY - size), (cX, cY + size), color, 5)


def escreve_texto(img, text, origem, color):
    """ faz a cruz no ponto cx cy"""

    font = cv2.FONT_HERSHEY_SIMPLEX
    origem = (0, 50)
    cv2.putText(img, str(text), origem, font, 1, color, 2, cv2.LINE_AA)




def image_da_webcam(img):
    # img = cv2.imread(img)

    image_lower = np.array([0])
    image_upper = np.array([254])

    # verde
    greenLower = (52, 86, 6)
    greenUpper = (87, 255, 255)

    # amarelo
    yellowLower = (24, 55, 55)
    yellowUpper = (50, 255, 255)


    mask_hsv = filtro_de_cor(img, yellowLower, yellowUpper)
    mask_hsv2 = filtro_de_cor(img, greenLower, greenUpper)

    mask = mascara_or(mask_hsv, mask_hsv2)


    contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    contornos_img = mask_rgb.copy()  # Cópia da máscara para ser desenhada "por cima"

    maior = []
    values = []
    maior_area = 0
    contador = 0;
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 4000:
            maior_area = area
            maior.append(c)
            contador = contador + 1

    # notamos que a função devolve um dicionario.
    x = 1
    for v in maior:

        cnt = v
        M = cv2.moments(cnt)

        # Calculo das coordenadas do centro de massa
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])


        ## para desenhar a cruz vamos passar a cor e o tamanho em pixel
        size = 20
        color = (128, 128, 0)

        cv2.line(contornos_img, (cx - size, cy), (cx + size, cy), color, 5)
        cv2.line(contornos_img, (cx, cy - size), (cx, cy + size), color, 5)

        # Para escrever vamos definir uma fonte

        if x == 1:
            x += 1
            color = (0, 255, 0)
            origem = (0, 25)

        else:
            x = 1
            color = (255, 0, 0)
            origem = (0, 50)


        font = cv2.FONT_HERSHEY_SIMPLEX
        text = cx, cy
        values.append(text)
        # origem = (0, 50)

        cv2.putText(contornos_img, str(text), origem, font, 1, color, 2, cv2.LINE_AA)

        cv2.drawContours(contornos_img, maior, -1, color, 5)

    contador = 0
    for v in values:
        temp = 0, 0
        if v != values[len(values) - 1]:
            temp = values[contador + 1]
            print(v, temp)
            cv2.line(contornos_img, v, temp, (67, 255, 255), 5)
            contador = contador + 1
        if v == values[len(values) - 1]:
            temp = values[len(values) - 1]
            angle_final = values[len(values) - 2]
            cv2.line(contornos_img, values[0], temp, (67, 255, 255), 5)
            angle_line = str(v).replace("(", "").replace(")", "").split(", ")
            angle_line2 = str(angle_final).replace("(", "").replace(")", "").split(", ")

            # angle = math.atan2(int(angle_line2[1]), int(angle_line2[0])) - math.atan2(int(angle_line[1]),
            #
            #                                                                         int(angle_line[0]))
            # print(angle)
            # if (angle < 0):
            #     angle_radians = -1 * math.ceil(math.degrees(angle))
            # angle_radians = math.ceil(math.degrees(angle))

            vY = int(angle_line2[1]) - int(angle_line[1])
            vX = int(angle_line2[0]) - int(angle_line[0])
            rad = math.atan2(vY, vX)
            angle = int(math.degrees(rad))
            if angle < 0:
                angle += 360
            print(angle)

            font = cv2.FONT_HERSHEY_SIMPLEX
            origem =  (0,100)

            cv2.putText(contornos_img, str(angle), origem, font, 2, (71, 255, 255), 5, cv2.LINE_AA)

    return contornos_img


cv2.namedWindow("preview")
# define a entrada de video para webcam
vc = cv2.VideoCapture(0)

# vc = cv2.VideoCapture("video.mp4") # para ler um video mp4

# configura o tamanho da janela
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 840)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 680)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    img = image_da_webcam(frame)  # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada

    cv2.imshow("preview", img)
    cv2.imshow("original", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
