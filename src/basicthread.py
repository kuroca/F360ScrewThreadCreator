import math

def height(pitch):
    return pitch * math.sqrt(3)/2

def minor_diameter(major_diameter,pitch):
    return round(major_diameter - (5/4)*height(pitch),2)
    
def pitch_diameter(major_diameter,pitch):
    height = pitch * math.sqrt(3)/2
    return round(major_diameter - (3/4)*height(pitch),2)