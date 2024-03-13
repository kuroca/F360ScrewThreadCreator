import math
import re
import basicthread as bt

def valid_tolerance_class(s):
    # Regular expression to match the tolerance class pattern
    # This pattern checks for a number between 3 and 9 followed by 'G', 'H', 'e', 'f', 'g', or 'h', respecting case sensitivity
    pattern = r"^[3-9][GHefgh]$"
    
    # Using re.match to check if the string matches the pattern without the IGNORECASE flag
    if re.match(pattern, s):
        return True
    else:
        return False

# Return is formatted as (tolerance_grade, tolerance_position)
def split_tolerance_class(tolerance_class):
    if(valid_tolerance_class(tolerance_class)):
        return (int(tolerance_class[0]), tolerance_class[1])
    else:
        raise ValueError("\"" + str(tolerance_class) + "\"" + " is not a valid tolerance class.")

# For external threads
def upper_fundamental_deviation(pitch,tolerance_class):
    
    tolerance_position = split_tolerance_class(tolerance_class)[1]

    match tolerance_position:
        case "e":
            k = 50 
        case "f":
            k = 30
        case "g":
            k = 15
        case "h":
            return 0
        case _:
            raise ValueError("\"" + str(tolerance_position) + "\"" + " is not a valid tolerance position.")
            
    return -1*(k + 11*pitch)/1000

# For internal threads    
def lower_fundamental_deviation(pitch,tolerance_class):

    tolerance_position = split_tolerance_class(tolerance_class)[1]
    
    match tolerance_position:
        case "G":
            return (15 + 11*pitch)/1000
        case "H":
            return 0
        case _:
            raise ValueError("\"" + str(tolerance_position) + "\"" + " is not a valid tolerance position.")

# Usage:
#
# (T_d)
#
# Pitch - The screw thread pitch
# Tolerance grade - The "number" part of the tolerance class, i.e. for tolerance class "6g", "6" is the tolerance grade
def external_major_diameter_tolerance(pitch,tolerance_class):

    tolerance_grade = split_tolerance_class(tolerance_class)[0]

    match tolerance_grade:
        case 4:
            k = 0.63
        case 6:
            k = 1
        case 8:
            k = 1.6
        case _:
            raise ValueError("\"" + str(tolerance_grade) + "\"" + " is not a valid tolerance grade.")
    return k*(180 * math.pow(pitch,2/3) - 3.15 * math.pow(pitch,-0.5))/1000


# Usage:
#
# (T_d2, T_D2)
#
# Pitch - The screw thread pitch
# Tolerance grade - The "number" part of the tolerance class, i.e. for tolerance class "6g", "6" is the tolerance grade
def pitch_diameter_tolerance(major_diameter,pitch,tolerance_class):

    tolerance_grade = split_tolerance_class(tolerance_class)[0]

    match tolerance_grade:
        case 3:
            k = 0.5
        case 4:
            k = 0.63
        case 5:
            k = 0.8
        case 6:
            k = 1
        case 7:
            k = 1.25
        case 8:
            k = 1.6
        case 9:
            k = 2
        case _:
            raise ValueError("\"" + str(tolerance_grade) + "\"" + " is not a valid tolerance grade.")
    return k*(90 * math.pow(pitch,0.4) * math.pow(major_diameter,0.1))/1000

# Usage:
#
# (T_D1)
#
# Pitch - The screw thread pitch
# Tolerance grade - The "number" part of the tolerance class, i.e. for tolerance class "6g", "6" is the tolerance grade    
def internal_minor_diameter_tolerance(pitch,tolerance_class):
    
    tolerance_grade = split_tolerance_class(tolerance_class)[0]
    
    match tolerance_grade:
        case 4:
            k = 0.63
        case 5:
            k = 0.8
        case 6:
            k=1
        case 7:
            k = 1.25
        case 8:
            k = 1.6
        case _:
            raise ValueError("\"" + str(tolerance_grade) + "\"" + " is not a valid tolerance grade.")
    if(pitch >= 1):
        return k * (230 * math.pow(pitch,0.7))/1000
    else:
        return k * (433 * pitch - 190 * math.pow(pitch,1.22))/1000

def external_major_diameter_max(major_diameter,pitch,tolerance_class):
    return major_diameter + upper_fundamental_deviation(pitch,tolerance_class)
    
def external_major_diameter_min(major_diameter,pitch,tolerance_class):
    return major_diameter + upper_fundamental_deviation(pitch,tolerance_class) - external_major_diameter_tolerance(pitch,tolerance_class)

def external_minor_diameter_max(major_diameter,pitch,tolerance_class):
    y = (pitch/8) * (1 - math.cos(math.pi/3 - math.acos(1 - pitch_diameter_tolerance(major_diameter,pitch,tolerance_class)/(pitch/2))))
        
    return bt.minor_diameter(major_diameter,pitch) - upper_fundamental_deviation(pitch,tolerance_class) - 2*y
    
def external_minor_diameter_min(major_diameter,pitch,tolerance_class):
    z = bt.height(pitch)/4 + pitch_diameter_tolerance(major_diameter,pitch,tolerance_class)/2 - pitch/8
        
    return bt.minor_diameter(major_diameter,pitch) - upper_fundamental_deviation(pitch,tolerance_class) - 2*z