import os
import math
import random
import time
import sys
import requests


#initialize stuff
width, height = os.get_terminal_size()
#multiply wdith height cause braille characters are 2x4
width = width * 2
height = height * 4
#initialize more
display = []
displayshader = []
alllinesegments = []

markerposx = 0
markerposy = 0
globallineopacity = 1
globallinewidth = 1
antialiasing = True
#global stage rotation vars
rotationX = 0
rotationY = 0
rotationZ = 0
lightvector = [1, 1, -2]
#all braille characters
unicodechars = [" ","\u2801","\u2802","\u2803","\u2804","\u2805","\u2806","\u2807","\u2808","\u2809","\u280A","\u280B","\u280C","\u280D","\u280E","\u280F","\u2810","\u2811","\u2812","\u2813","\u2814","\u2815","\u2816","\u2817","\u2818","\u2819","\u281A","\u281B","\u281C","\u281D","\u281E","\u281F","\u2820","\u2821","\u2822","\u2823","\u2824","\u2825","\u2826","\u2827","\u2828","\u2829","\u282A","\u282B","\u282C","\u282D","\u282E","\u282F","\u2830","\u2831","\u2832","\u2833","\u2834","\u2835","\u2836","\u2837","\u2838","\u2839","\u283A","\u283B","\u283C","\u283D","\u283E","\u283F","\u2840","\u2841","\u2842","\u2843","\u2844","\u2845","\u2846","\u2847","\u2848","\u2849","\u284A","\u284B","\u284C","\u284D","\u284E","\u284F","\u2850","\u2851","\u2852","\u2853","\u2854","\u2855","\u2856","\u2857","\u2858","\u2859","\u285A","\u285B","\u285C","\u285D","\u285E","\u285F","\u2860","\u2861","\u2862","\u2863","\u2864","\u2865","\u2866","\u2867","\u2868","\u2869","\u286A","\u286B","\u286C","\u286D","\u286E","\u286F","\u2870","\u2871","\u2872","\u2873","\u2874","\u2875","\u2876","\u2877","\u2878","\u2879","\u287A","\u287B","\u287C","\u287D","\u287E","\u287F","\u2880","\u2881","\u2882","\u2883","\u2884","\u2885","\u2886","\u2887","\u2888","\u2889","\u288A","\u288B","\u288C","\u288D","\u288E","\u288F","\u2890","\u2891","\u2892","\u2893","\u2894","\u2895","\u2896","\u2897","\u2898","\u2899","\u289A","\u289B","\u289C","\u289D","\u289E","\u289F","\u28A0","\u28A1","\u28A2","\u28A3","\u28A4","\u28A5","\u28A6","\u28A7","\u28A8","\u28A9","\u28AA","\u28AB","\u28AC","\u28AD","\u28AE","\u28AF","\u28B0","\u28B1","\u28B2","\u28B3","\u28B4","\u28B5","\u28B6","\u28B7","\u28B8","\u28B9","\u28BA","\u28BB","\u28BC","\u28BD","\u28BE","\u28BF","\u28C0","\u28C1","\u28C2","\u28C3","\u28C4","\u28C5","\u28C6","\u28C7","\u28C8","\u28C9","\u28CA","\u28CB","\u28CC","\u28CD","\u28CE","\u28CF","\u28D0","\u28D1","\u28D2","\u28D3","\u28D4","\u28D5","\u28D6","\u28D7","\u28D8","\u28D9","\u28DA","\u28DB","\u28DC","\u28DD","\u28DE","\u28DF","\u28E0","\u28E1","\u28E2","\u28E3","\u28E4","\u28E5","\u28E6","\u28E7","\u28E8","\u28E9","\u28EA","\u28EB","\u28EC","\u28ED","\u28EE","\u28EF","\u28F0","\u28F1","\u28F2","\u28F3","\u28F4","\u28F5","\u28F6","\u28F7","\u28F8","\u28F9","\u28FA","\u28FB","\u28FC","\u28FD","\u28FE","\u28FF"]



#function to reset display array, otherwize itll be drawing over itself
#display array is 2d up to width*2, height*4. 0 for pixel off and 1 for on. start with all 0
def cleardisplay():
    global width
    global height
    width, height = os.get_terminal_size()
    #multiply wdith height cause braille characters are 2x4
    width = width * 2
    height = height * 4
    global display
    global displayshader
    global alllinesegments
    display = []
    displayshader = []
    alllinesegments = []
    for a in range(width):
        display.append([])
        displayshader.append([])
        for b in range(height):
            display[a].append(0)
            displayshader[a].append(0)
cleardisplay()

#function to write display array to screen
def render():
    this = ""
    displayflip = [x for x in zip(*display)]
    for b in range(int(height / 4)):
        if (sum(displayflip[b * 4]) + sum(displayflip[b * 4 + 1]) + sum(displayflip[b * 4 + 2]) + sum(displayflip[b * 4 + 3]) == 0):
            this += "\n"
            continue
        for a in range(int(width / 2)):
            basex = a * 2
            basey = b * 4
            #determine correct braille character based on grouped 2x4 pixels
            sumnum = (display[basex][basey]) + (display[basex][basey + 1] * 2) + (display[basex][basey + 2] * 4) + (display[basex + 1][basey] * 8) + (display[basex + 1][basey + 1] * 16) + (display[basex + 1][basey + 2] * 32) + (display[basex][basey + 3] * 64) + (display[basex + 1][basey + 3] * 128)
            #get alpha
            if (antialiasing):
                sumalpha = (displayshader[basex][basey] + displayshader[basex][basey + 1] + displayshader[basex][basey + 2] + displayshader[basex + 1][basey] + displayshader[basex + 1][basey + 1] + displayshader[basex + 1][basey + 2] + displayshader[basex][basey + 3] + displayshader[basex + 1][basey + 3]) / 8
            else:
                alphacount = 0
                sumalpha = 0
                for alpha in range(8):
                    thisalpha = displayshader[basex + math.floor(alpha / 4)][basey + (alpha % 4)]
                    if (thisalpha > 0):
                        alphacount += 1
                        sumalpha += thisalpha
                if (alphacount == 0):
                    sumalpha = 0
                else:
                    sumalpha /= alphacount

            alpha = int(min(max(sumalpha * 24, 0), 23))
            #append it to "this"
            if (sumnum == 0):
                this += " "
            else:
                this +=  "\x1b[38;5;" + str(alpha + 232) + "m" + unicodechars[sumnum]
            #this +=  unicodechars[sumnum]
    #print braille to screen
    print(this)

#function to get intersection point between 2 lines. used in unfinished fill function
def oldgetIntersectPoint(line1AX, line1AY, line1BX, line1BY, line2AX, line2AY, line2BX, line2BY):
    line1AX += 0.01
    line1AY += 0.01
    line2AX -= 0.02
    line2AY -= 0.02
    m = ((line1BY - line1AY) / (line1BX - line1AX))
    n = (((line1AY * line1BX) - (line1AX * line1BY)) / (line1BX - line1AX))
    o = ((line2BY - line2AY) / (line2BX - line2AX))
    p = (((line2AY * line2BX) - (line2AX * line2BY)) / (line2BX - line2AX))
    intersectX = (n - p) / (o - m)
    intersectY = ((n * o) - (m * p)) / (o - m)
    isBounded = (intersectX > min(line1AX, line1BX) and intersectX < max(line1AX, line1BX) and intersectY > min(line1AY, line1BY) and intersectY < max(line1AY, line1BY) and intersectX > min(line2AX, line2BX) and intersectX < max(line2AX, line2BX) and intersectY > min(line2AY, line2BY) and intersectY < max(line2AY, line2BY))
    return([intersectX, intersectY, isBounded])

def getIntersectPoint(a, b, c, d, f, g, h, i):
    a += 0.01
    b += 0.01
    f -= 0.02
    g -= 0.02
    X = ((b * c - a * d) * (h - f) - (g * h - f * i) * (c - a)) / ((c - a) * (i - g) - (h - f) * (d - b))
    Y = ((b * c - a * d) * (i - g) - (g * h - f * i) * (d - b)) / ((c - a) * (i - g) - (h - f) * (d - b))
    isBounded = (X > min(a, c) and X < max(a, c) and Y > min(b, d) and Y < max(b, d) and X > min(f, h) and X < max(f, h) and Y > min(g, i) and Y < max(g, i))
    return([X, Y, isBounded])

#move marker to xy like in canvas
def moveTo(x, y):
    global markerposx
    global markerposy
    global alllinesegments
    alllinesegments = []
    markerposx = int(x)
    markerposy = int(y)

#draw line from markerpos's to nx and ny
def oldlineTo(nx, ny):
    global markerposx
    global markerposy
    nx = int(nx)
    ny = int(ny)

    #step algorithm for drawing lines
    currentx = markerposx
    currenty = markerposy
    if (abs(markerposx - nx) > abs(markerposy - ny)):
        if ((nx - markerposx) == 0):
            return
        slope = ((ny - markerposy) / (nx - markerposx))
        for x in range(abs(markerposx - nx)):
            if (x < 0):
                x = 0
            if (nx < markerposx):
                currentx -= 1
                currenty -= slope
            else:
                currentx += 1
                currenty += slope
            
            if (currentx >= 0 and currentx < width and currenty >= 0 and currenty < height):
                #if a point is on the line, set that xy to 1 in "display"
                display[currentx][int(currenty)] = 1
    else:
        if ((ny - markerposy) == 0):
            return
        slope = ((nx - markerposx) / (ny - markerposy))
        for y in range(abs(markerposy - ny)):
            if (y < 0):
                y = 0
            if (ny < markerposy):
                currenty -= 1
                currentx -= slope
            else:
                currenty += 1
                currentx += slope
            if (currentx >= 0 and currentx < width and currenty >= 0 and currenty < height):
                #if a point is on the line, set that xy to 1 in "display"
                display[int(currentx)][currenty] = 1
    #set new marker position
    markerposx = nx
    markerposy = ny

def lineTo(nx, ny):
    global markerposx
    global markerposy
    global globallineopacity
    globallineopacity = max(globallineopacity, 0)
    x1 = markerposx
    y1 = markerposy
    x2 = int(nx)
    y2 = int(ny)
    alllinesegments.append([markerposx, markerposy, x2, y2])
    markerposx = int(nx)
    markerposy = int(ny)
    if (x1 > x2):
        x1, x2 = x2, x1
        y1, y2 = y2, y1


    if ((x1 < 0 and x2 < 0) or (x1 > width and x2 > width) or (y1 < 0 and y2 < 0) or (y1 > height and y2 > height)):
        return


    if (abs(x1 - x2) > abs(y1 - y2)):
        if ((x2 - x1) == 0):
            return
        if (y2 > y1):
            #SLOPING FORWARD DOWN
            slope = ((y2 - y1) / (x2 - x1))
            if (x1 < 0):
                y1 -= int(x1 * slope)
                x1 = 0
            if (x2 >= width):
                y2 += int((x2 - width) * slope)
                x2 = width - 2
                
            ythreshold = 0.5
            yfloat = 0
            for x in range(x1, x2 + 1):
                for w in range(globallinewidth):
                    if (y1 + w >= 0 and y1 + w < height):
                        display[x][y1 + w] = 1
                        displayshader[x][y1 + w] += globallineopacity
                yfloat += slope
                if (yfloat >= ythreshold):
                    y1 += 1
                    ythreshold += 1
        else:
            #SLOPING FORWARD UP
            slope = ((y2 - y1) / (x2 - x1))
            if (x1 < 0):
                y1 -= int(x1 * slope)
                x1 = 0
            if (x2 >= width):
                y2 -= int((x2 - width) * slope)
                x2 = width - 2

            ythreshold = 0.5
            yfloat = 0
            for x in range(x1, x2 + 1):
                for w in range(globallinewidth):
                    if (y1 + w >= 0 and y1 + w < height):
                        display[x][y1 + w] = 1
                        displayshader[x][y1 + w] += globallineopacity
                yfloat -= slope
                if (yfloat >= ythreshold):
                    y1 -= 1
                    ythreshold += 1
    else:
        if ((y2 - y1) == 0):
                return
        if (y2 > y1):
            #SLOPING DOWN FORWARD
            slope = ((x2 - x1) / (y2 - y1))
            if (y1 < 0):
                x1 -= int(y1 * slope)
                y1 = 0
            if (y2 >= height):
                x2 += int((y2 - height) * slope)
                y2 = height - 2

            xthreshold = 0.5
            xfloat = 0
            for y in range(y1, y2 + 1):
                for w in range(globallinewidth):
                    if (x1 + w >= 0 and x1 + w < width):
                        display[x1 + w][y] = 1
                        displayshader[x1 + w][y] += globallineopacity
                xfloat += slope
                if (xfloat >= xthreshold):
                    x1 += 1
                    xthreshold += 1
        if (y2 < y1):
            #SLOPING UP FORWARD
            slope = ((x2 - x1) / (y2 - y1))
            
            if (y2 < 0):
                x2 -= int(y2 * slope)
                y2 = 0
            if (y1 >= height):
                x1 += int((y1 - height) * slope)
                y1 = height - 1
            xthreshold = 0.5
            xfloat = 0
            x1, x2 = x2, x1
            for y in range(y2, y1):
                for w in range(globallinewidth):
                    if (x1 + w >= 0 and x1 + w < width):
                        display[x1 + w][y] = 1
                        displayshader[x1 + w][y] += globallineopacity
                xfloat -= slope
                if (xfloat >= xthreshold):
                    x1 -= 1
                    xthreshold += 1

#unfinished fill function
def sfill(opacity=1):
    global alllinesegments
    alllinesegments.append([markerposx, markerposy, alllinesegments[0][0], alllinesegments[0][1]])
    for xy in range(width * height):
        x = math.floor(xy / height)
        y = xy % height
        intcount = 0
        for l in alllinesegments:
            intsec = getIntersectPoint(l[0], l[1], l[2], l[3], x, y, x + 2000, y)
            if (intsec[2] == True):
                intcount += 1
        if (intcount % 2 == 1):
            display[x][y] = 1
            displayshader[x][y] = opacity
    
def fill(opacity=1):
    global alllinesegments
    alllinesegments.append([markerposx, markerposy, alllinesegments[0][0], alllinesegments[0][1]])
    for y in range(height):
        intersectXs = []
        for l in alllinesegments:
            intsec = getIntersectPoint(l[0], l[1], l[2], l[3], -2000, y, width + 2000, y)
            if (intsec[2] == True):
                intersectXs.append(round(intsec[0]))
        intersectXs.sort()
        for i in range(0, len(intersectXs), 2):
            for x in range(min(width, max(0, intersectXs[i])), min(width, max(0, intersectXs[i + 1]))):
                display[x][y] = 1
                displayshader[x][y] = opacity
        

#function from internet to apply rotations to a 3d vector
def applyrotation(x, y, z, rotX, rotY, rotZ):
    cosa = math.cos(rotZ)
    sina = math.sin(rotZ)
    cosb = math.cos(rotY)
    sinb = math.sin(rotY)
    cosc = math.cos(rotX)
    sinc = math.sin(rotX)
    Axx = cosa*cosb
    Axy = cosa*sinb*sinc - sina*cosc
    Axz = cosa*sinb*cosc + sina*sinc
    Ayx = sina*cosb
    Ayy = sina*sinb*sinc + cosa*cosc
    Ayz = sina*sinb*cosc - cosa*sinc
    Azx = -sinb
    Azy = cosb*sinc
    Azz = cosb*cosc
    newx = Axx*x + Axy*y + Axz*z
    newy = Ayx*x + Ayy*y + Ayz*z
    newz = Azx*x + Azy*y + Azz*z
    return([newx, newy, newz]) 

#2d projection based on the perspective var
def convert3dto2d(x, y, z):
    perspective = 400
    #apply stage rotations
    newcoords = applyrotation(x, y, z, rotationX, rotationY, rotationZ)
    #maths
    middle = [width / 2, height / 2]
    pers = perspective / (perspective - newcoords[2])
    if (newcoords[2] > perspective):
      pers = 1000000
    
    newx = ((newcoords[0]) * pers) + middle[0]
    newy = ((newcoords[1]) * pers) + middle[1]
    #return 2d coordinates
    return([newx, newy])

#same as moveTo() but z
def moveTo3d(x, y, z):
    newpos = convert3dto2d(x, y, z)
    moveTo(newpos[0], newpos[1])

#same as lineTo() but z
def lineTo3d(x, y, z):
    newpos = convert3dto2d(x, y, z)
    #newpos = [x, y]
    lineTo(newpos[0], newpos[1])

#draws a frame of a 2d rectangle in 3d space
def rect(x, y, z, width, height, rotX, rotY, rotZ, rotmid=False):
    coords = [[x, y, z], [x + width, y, z], [x + width, y + height, z], [x, y + height, z]]
    if (rotmid):
        v1 = applyrotation(-width / 2, -height / 2, 0, rotX, rotY, rotZ)
        v2 = applyrotation(width / 2, -height / 2, 0, rotX, rotY, rotZ)
        v3 = applyrotation(width / 2, height / 2, 0, rotX, rotY, rotZ)
        v4 = applyrotation(-width / 2, height / 2, 0, rotX, rotY, rotZ)
    else:
        v1 = applyrotation(0, 0, 0, rotX, rotY, rotZ)
        v2 = applyrotation(width, 0, 0, rotX, rotY, rotZ)
        v3 = applyrotation(width, height, 0, rotX, rotY, rotZ)
        v4 = applyrotation(0, height, 0, rotX, rotY, rotZ)
    
    moveTo3d(v1[0] + x, v1[1] + y, v1[2] + z)
    lineTo3d(v2[0] + x, v2[1] + y, v2[2] + z)
    lineTo3d(v3[0] + x, v3[1] + y, v3[2] + z)
    lineTo3d(v4[0] + x, v4[1] + y, v4[2] + z)
    lineTo3d(v1[0] + x, v1[1] + y, v1[2] + z)

#draws a frame of a 3d rectangle
def rect3d(x, y, z, width, height, depth, rotX, rotY, rotZ, rotmid=False):
    #apply local rotation to 8 points
    coords = [[x, y, z], [x + width, y, z], [x + width, y + height, z], [x, y + height, z], [x, y, z + depth], [x + width, y, z + depth], [x + width, y + height, z + depth], [x, y + height, z + depth]]
    if (rotmid):
        v1 = applyrotation(-width / 2, -height / 2, -depth / 2, rotX, rotY, rotZ)
        v2 = applyrotation(width / 2, -height / 2, -depth / 2, rotX, rotY, rotZ)
        v3 = applyrotation(width / 2, height / 2, -depth / 2, rotX, rotY, rotZ)
        v4 = applyrotation(-width / 2, height / 2, -depth / 2, rotX, rotY, rotZ)
        v5 = applyrotation(-width / 2, -height / 2, depth / 2, rotX, rotY, rotZ)
        v6 = applyrotation(width / 2, -height / 2, depth / 2, rotX, rotY, rotZ)
        v7 = applyrotation(width / 2, height / 2, depth / 2, rotX, rotY, rotZ)
        v8 = applyrotation(-width / 2, height / 2, depth / 2, rotX, rotY, rotZ)
    else:
        v1 = applyrotation(0, 0, 0, rotX, rotY, rotZ)
        v2 = applyrotation(width, 0, 0, rotX, rotY, rotZ)
        v3 = applyrotation(width, height, 0, rotX, rotY, rotZ)
        v4 = applyrotation(0, height, 0, rotX, rotY, rotZ)
        v5 = applyrotation(0, 0, depth, rotX, rotY, rotZ)
        v6 = applyrotation(width, 0, depth, rotX, rotY, rotZ)
        v7 = applyrotation(width, height, depth, rotX, rotY, rotZ)
        v8 = applyrotation(0, height, depth, rotX, rotY, rotZ)
    #draw edges of new points
    moveTo3d(v1[0] + x, v1[1] + y, v1[2] + z)
    lineTo3d(v2[0] + x, v2[1] + y, v2[2] + z)
    lineTo3d(v3[0] + x, v3[1] + y, v3[2] + z)
    lineTo3d(v4[0] + x, v4[1] + y, v4[2] + z)
    lineTo3d(v1[0] + x, v1[1] + y, v1[2] + z)
    lineTo3d(v5[0] + x, v5[1] + y, v5[2] + z)
    lineTo3d(v6[0] + x, v6[1] + y, v6[2] + z)
    lineTo3d(v7[0] + x, v7[1] + y, v7[2] + z)
    lineTo3d(v8[0] + x, v8[1] + y, v8[2] + z)
    lineTo3d(v5[0] + x, v5[1] + y, v5[2] + z)
    moveTo3d(v2[0] + x, v2[1] + y, v2[2] + z)
    lineTo3d(v6[0] + x, v6[1] + y, v6[2] + z)
    moveTo3d(v4[0] + x, v4[1] + y, v4[2] + z)
    lineTo3d(v8[0] + x, v8[1] + y, v8[2] + z)
    moveTo3d(v3[0] + x, v3[1] + y, v3[2] + z)
    lineTo3d(v7[0] + x, v7[1] + y, v7[2] + z)
    
#cross product 3d formula
def crossproduct(o1, o2, o3, a1, a2, a3, b1, b2, b3):
  a1 -= o1
  a2 -= o2
  a3 -= o3
  b1 -= o1
  b2 -= o2
  b3 -= o3
  newx = a2 * b3 - a3 * b2
  newy = a3 * b1 - a1 * b3
  newz = a1 * b2 - a2 * b1
  return([newx, newy, newz])

#2d angle formula with normalized 3d vector
def anglenormal(a1, a2, a3, b1, b2, b3):
    magA = math.sqrt(a1*a1 + a2*a2 + a3*a3)
    magB = math.sqrt(b1*b1 + b2*b2 + b3*b3)
    a1 /= magA
    a2 /= magA
    a3 /= magA
    b1 /= magB
    b2 /= magB
    b3 /= magB
    angle = (2 * math.asin((a1 * b1) + (a2 * b2) + (a3 * b3))) / math.pi
    return(angle)

#make arr of faces from a .obj
def makefromobj(txt):
    txt = txt.replace("  ", " ")
    txt = txt.replace(" \n", "\n")
    faces = []
    vertices = []
    for line in txt.split("\n"):
        #print(line)
        if (line[:2] == "v "):
            vertex = line[2:].split(" ")
            vertices.append(vertex)
        elif (line[:2] == "f "):
            face = []
            #print(vertices)
            for vertex_info in line[2:].split(" "):
                #print(vertex_info)
                vertex_index = int(vertex_info.split("/")[0]) - 1
                corresponding_vertex = vertices[vertex_index]
                face.append(corresponding_vertex)
            faces.append(face)
    return(faces)

#draw all faces of a makefromobj() arr
def drawobj(arr, scale):
    global globallineopacity
    global rotationX
    global rotationY
    global rotationZ
    #sort faces by z
    allfaces = []
    for f in arr:
        thisz = 0
        for v in range(0, len(f)):
            thisz += applyrotation(float(f[v][0]) * scale, float(f[v][1]) * -scale, float(f[v][2]) * scale, rotationX, rotationY, rotationZ)[2] + 5000
        thisz /= len(f)
        allfaces.append([f, thisz])
    allfaces = sorted(allfaces, key=lambda x: -x[1], reverse=True)

    for f in allfaces:
        thisz = f[1]
        f = f[0]

        minsoften = 0.2
        #globallineopacity = (thisz - 5000 + scale) / (scale * 2)
        originrotated = applyrotation(float(f[1][0]) * scale, float(f[1][1]) * -scale, float(f[1][2]) * scale, rotationX, rotationY, rotationZ)
        cross1rotated = applyrotation(float(f[0][0]) * scale, float(f[0][1]) * -scale, float(f[0][2]) * scale, rotationX, rotationY, rotationZ)
        cross2rotated = applyrotation(float(f[2][0]) * scale, float(f[2][1]) * -scale, float(f[2][2]) * scale, rotationX, rotationY, rotationZ)
        cross = crossproduct(originrotated[0], originrotated[1], originrotated[2], cross1rotated[0], cross1rotated[1], cross1rotated[2], cross2rotated[0], cross2rotated[1], cross2rotated[2])
        anglealpha = -(anglenormal(cross[0], cross[1], cross[2], lightvector[0], lightvector[1], lightvector[2]))
        globallineopacity = 0
        
        moveTo3d(float(f[0][0]) * scale, float(f[0][1]) * -scale, float(f[0][2]) * scale)
        for v in range(1, len(f)):
            lineTo3d(float(f[v][0]) * scale, float(f[v][1]) * -scale, float(f[v][2]) * scale)
        lineTo3d(float(f[0][0]) * scale, float(f[0][1]) * -scale, float(f[0][2]) * scale)

        
        fill(anglealpha)
        
        #fill((thisz - 5000 + scale) / (scale * 2))
        #fill(anglealpha * (1 - minsoften) + minsoften)





# ---- PLAYGROUND ----
'''moveTo(10, 50)
oldlineTo(20, 10)
render()
time.sleep(0.5)
moveTo(30, 50)
lineTo(40, 10)
render()'''

#line going clockwise
def rentestline():
    index = 0
    while True:
        cleardisplay()
        moveTo(width / 2, height / 2)
        lineTo(width / 2 + (math.sin(index * 0.1) * 50), height / 2 + (math.cos(index * 0.1) * 50))
        render()
        time.sleep(0.01)
        index += 0.2

#triangle prism
def rentesttriangle():
    global rotationX, rotationY
    index = 0
    while True:
        cleardisplay()
        moveTo3d(-30, 0, -30)
        lineTo3d(30, 0, -30)
        lineTo3d(0, 0, 30)
        lineTo3d(-30, 0, -30)
        lineTo3d(0, -45, 0)
        lineTo3d(30, 0, -30)
        moveTo3d(0, -45, 0)
        lineTo3d(0, 0, 30)

        rotationX = index * 0.2
        rotationY = index * 0.4
        render()
        #time.sleep(0.01)
        index += 0.04

#three spinning cubes
def rentestcubes():
    global rotationY
    index = 0
    while True:
        cleardisplay()
        rect3d(-40, 0, -40, 30, 30, 30, index * -1, 0, 0, True)
        rect3d(0, 0, 0, 30, 30, 30, 0, 0, 0, True)
        rect3d(40, 0, 40, 30, 30, 30, index * 1, 0, 0, True)

        rotationY = index * 0.4
        render()
        
        #time.sleep(0.001)
        index += 0.04

#spinning rectangle
def rentestrect():
    global rotationY
    index = 0
    while True:
        cleardisplay()
        for i in range(1):
            rect(0, 0, 0, width/3, width/3, index * -3, 0, 0, True)
            #lineTo3d(200, 200, 100)
            #lineTo3d(0, 0, -50)
        fill()
        rotationY = index * 0.8
        render()
        
        time.sleep(0.01)
        index += 0.01


#double pendulum
def rentestpendulum():
    global globallineopacity
    globallineopacity = 0.02
    g = 0.12
    angOffset = 0.000001
    ballSize = 0
    allPens = []
    pensCount = 10000
    for a in range(pensCount):
        len1 = int(height / 5)
        len2 = int(height / 5)
        ang1 = math.pi * 3 / 4 + (a * angOffset)
        ang2 = math.pi * 3 / 4 + (a * angOffset)
        m1 = 9
        m2 = 9
        angacc1 = 0
        angacc2 = 0
        angv1 = 0
        angv2 = 0
        ballcords1 = [0, 0]
        ballcords2 = [0, 0]
        allPens.append([len1, len2, ang1, ang2, m1, m2, angacc1, angacc2, angv1, angv2, ballcords1, ballcords2])

    while True:
        cleardisplay()
        startPoint = [width / 2, height / 2]
        for a in range(pensCount):
            thisobj = allPens[a]
            penpoint2 = allPens[a][2]
            penpoint3 = allPens[a][3]
            penpoint4 = allPens[a][4]
            penpoint5 = allPens[a][5]
            penpoint6 = allPens[a][6]
            penpoint7 = allPens[a][7]
            penpoint8 = allPens[a][8]
            penpoint9 = allPens[a][9]
            #new line fill
            moveTo(startPoint[0], startPoint[1])
            lineTo(allPens[a][10][0], allPens[a][10][1])
            lineTo(allPens[a][11][0], allPens[a][11][1])
            allPens[a][10][0] = startPoint[0] + (math.sin(penpoint2) * thisobj[0])
            allPens[a][10][1] = startPoint[1] + (math.cos(penpoint2) * thisobj[0])
            allPens[a][11][0] = startPoint[0] + (math.sin(penpoint2) * thisobj[0]) + (math.sin(penpoint3) * thisobj[1])
            allPens[a][11][1] = startPoint[1] + (math.cos(penpoint2) * thisobj[0]) + (math.cos(penpoint3) * thisobj[1])
            num1 = -g * (2 * penpoint4 + penpoint5) * math.sin(penpoint2)
            num2 = -penpoint5 * g * math.sin(penpoint2 - 2 * penpoint3)
            num3 = -2 * math.sin(penpoint2 - penpoint3)
            num4 = penpoint5 * ((pow(penpoint9, 2) * thisobj[1]) + (pow(thisobj[8], 2) * thisobj[0] * math.cos(penpoint2 - penpoint3)))
            den = thisobj[0] * (2 * penpoint4 + penpoint5 - penpoint5 * math.cos(2 * penpoint2 - 2 * penpoint3))
            penpoint6 = (num1 + num2 + num3 * num4) / den
            num1 = 2 * math.sin(penpoint2 - penpoint3)
            num2 = pow(thisobj[8], 2) * thisobj[0] * (penpoint4 + penpoint5)
            num3 = g * (penpoint4 + penpoint5) * math.cos(penpoint2)
            num4 = pow(penpoint9, 2) * thisobj[1] * penpoint5 * math.cos(penpoint2 - penpoint3)
            den = thisobj[1] * (2 * penpoint4 + penpoint5 - penpoint5 * math.cos(2 * penpoint2 - 2 * penpoint3))
            penpoint7 = (num1 * (num2 + num3 + num4)) / den
            thisobj[8] += penpoint6
            thisobj[9] += penpoint7
            thisobj[2] += thisobj[8]
            thisobj[3] += thisobj[9]
        render()
        time.sleep(0.01)

#monkey / lego / cube
def rentestobjfile(filepath, scale):
    global rotationX
    global rotationY
    global lightvector
    f = open(filepath, "r").read()
    myobj = makefromobj(f)
    index = 0
    intindex = 0
    while True:
        cleardisplay()
        drawobj(myobj, scale)
        rotationY = index * 2
        #rotationY = math.pi * 1
        rotationX = index * 1.2
        render()
        index += 0.03
        intindex += 1
        '''if (intindex % 10 == 1):
            response = requests.get("https://jsonblob.com/api/jsonBlob/893277666019655680").json()["vector"]
            if (response[0] == 0) and (response[1] == 0) and (response[2] == 0):
                lightvector = [0, 0, -1]
            else:
                lightvector = response'''
        
        time.sleep(0.01)


globallineopacity = 1
#rentestobjfile("/Users/Charlie/Downloads/lego.obj", height * 0.008)
rentestobjfile("/Users/Charlie/Downloads/monkey.obj", height * 0.3)
#rentestobjfile("/Users/Charlie/Downloads/cube.obj", height * 0.2)
#rentestobjfile("/Users/Charlie/Downloads/Nintendo 64 - Super Mario 64 - Mario/mario64.obj", height * 0.002)
#rentestobjfile("/Users/Charlie/Downloads/Bob-omb Battlefield/Bob-omb Battlefield.obj", height * 0.05)
#rentestline()
#rentesttriangle()
#rentestcubes()
#rentestrect()
#rentestpendulum()

