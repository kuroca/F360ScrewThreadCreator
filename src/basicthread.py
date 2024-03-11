import math

def minor_diameter(major_diameter,pitch):
    height = thread_pitch * math.sqrt(3)/2
    return round(major_diameter - (5/4)*height,2)
    
def pitch_diameter(major_diameter,pitch)
    height = thread_pitch * math.sqrt(3)/2
    return round(major_diameter - (3/4)*height,2)