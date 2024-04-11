from lxml import etree

def unformat(s):
    lines = s.split('\n')
    
    stripped_lines = [line.lstrip() for line in lines]
    
    result = ''.join(stripped_lines)
    
    return result

def create_ThreadSize(major_diameter):
    new_ts = etree.Element("ThreadSize")
    etree.SubElement(new_ts, "Size").text = str(major_diameter)
    return new_ts

def create_Designation(major_diameter,pitch):
    new_d = etree.Element("Designation")
    etree.SubElement(new_d, "ThreadDesignation").text = "M" + str(major_diameter) + "x" + str(pitch)
    etree.SubElement(new_d, "CTD").text = "M" + str(major_diameter) + "x" + str(pitch)
    etree.SubElement(new_d, "Pitch").text = str(pitch)
    return new_d
    
def insert_thread_listing(xml_file,major_diameter,pitch,tolerance_class):
    tree = etree.fromstring(xml_file)    
    
    # Check if the major diameter is listed in the file
    md_found = False
    for i in range(len(tree.xpath('/ThreadType/ThreadSize/Size'))):
        if(float(tree.xpath('/ThreadType/ThreadSize/Size')[i].text) == major_diameter):
            md_found = i
    
    # If not found, create a listing with major diameter
    if(md_found == False):
        tree.xpath('/ThreadType')[0].append(create_Designation(major_diameter,pitch))
    else:
        # If found, check if the pitch is listed under that diameter
        p_found = False