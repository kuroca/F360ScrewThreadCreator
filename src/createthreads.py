import xml.etree.ElementTree as ET
from xml.dom import minidom
import math
import os
import shutil
from pathlib import Path
import getpass

def updatefusionthreads(filename):
    # Replace '[user name]' with the actual user name or dynamically fetch the current user's username
    user_name = getpass.getuser()

    # Define the source file path
    source_file = filename

    # Define the base directory path dynamically using the user's name
    base_dir = f"C:/Users/Tyler/AppData/Local/Autodesk/webdeploy/production/"

    # Function to copy the file to the destination
    def copy_file_to_directory(build_dir):
        destination_dir = os.path.join(build_dir, "Fusion/Server/Fusion/Configuration/ThreadData")
        os.makedirs(destination_dir, exist_ok=True)  # Create the destination directory if it doesn't exist
        shutil.copy(source_file, destination_dir)
        print(f"File copied to {destination_dir}")

    # Iterate over all subdirectories in the base directory
    for subdir in next(os.walk(base_dir))[1]:
        build_dir_path = os.path.join(base_dir, subdir)
        copy_file_to_directory(build_dir_path)

def prettify(elem):
    """Return a pretty-printed XML string for the element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def remove_blank_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        non_blank_lines = [line for line in lines if line.strip()]

    with open(file_path, 'w') as file:
        file.writelines(non_blank_lines)

def thread_dimensions(thread_diameter,thread_pitch):
    height = thread_pitch * math.sqrt(3)/2
    
    basic_minor_diameter = thread_diameter - (5/4)*height
    basic_pitch_diameter = thread_diameter - (3/4)*height
    
    return (round(basic_minor_diameter,2),round(basic_pitch_diameter,2))

def add_thread_size(filename, diameter, pitch):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except FileNotFoundError:
        root = ET.Element("ThreadType")
        root.append(ET.Element("Name", text="Camera Screw Threads"))
        root.append(ET.Element("CustomName", text="Camera Screw Threads"))
        root.append(ET.Element("Unit", text="mm"))
        root.append(ET.Element("Angle", text="60"))
        root.append(ET.Element("SortOrder", text="15"))
        tree = ET.ElementTree(root)
    
    d1,d2 = thread_dimensions(diameter,pitch)
    
    thread_size = ET.SubElement(root, "ThreadSize")
    size = ET.SubElement(thread_size, "Size")
    size.text = f"{diameter:.2f}"

    designation = ET.SubElement(thread_size, "Designation")
    thread_designation = ET.SubElement(designation, "ThreadDesignation")
    thread_designation.text = f"M{diameter:.2f}x{pitch:.2f}"

    ctd = ET.SubElement(designation, "CTD")
    ctd.text = f"M{diameter}x{pitch}"

    pitch_element = ET.SubElement(designation, "Pitch")
    pitch_element.text = f"{pitch:.2f}"

    for gender, thread_class in [("external", "6g"), ("internal", "6H")]:
        thread = ET.SubElement(designation, "Thread")
        ET.SubElement(thread, "Gender").text = gender
        ET.SubElement(thread, "Class").text = thread_class
        ET.SubElement(thread, "MajorDia").text = f"{diameter:.2f}"
        # Example values for PitchDia and MinorDia, adjust calculation as needed
        ET.SubElement(thread, "PitchDia").text = f"{d2:.2f}"
        ET.SubElement(thread, "MinorDia").text = f"{d1:.2f}"

    with open(filename, "w") as xml_file:
        xml_file.write(prettify(root))
        
    remove_blank_lines(filename)

# Example usage:
filename = "CameraScrewThreads.xml"
diameter = float(input("Thread diameter: "))
pitch = float(input("Thread pitch: "))
add_thread_size(filename, diameter, pitch)
updatefusionthreads(filename)
