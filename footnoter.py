import zipfile
import xml.etree.ElementTree as ET
import sys

NAMESPACE={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def extract_footnotes(docx_path):
    """Funtion extract_footnotes(docx_path)
    Extracts all the footnotes in a docx document
    
    Input 
    docx_path: string, the path to the docx file.
    
    Output
    A list of string, each one is a footnote.
    """
    footnotes=[]
    with zipfile.ZipFile(docx_path, 'r') as docx:
        try:
            footnotes_xml = docx.read('word/footnotes.xml')
            tree = ET.ElementTree(ET.fromstring(footnotes_xml))
            root = tree.getroot()
            for footnote in root.findall('w:footnote', NAMESPACE):
                text_elements = footnote.findall('.//w:t', NAMESPACE)
                footnote_text = ''.join([text.text for text in text_elements if text.text])
                footnotes.append(footnote_text)
        except KeyError:
            print("No footnotes found in the document.")
    return footnotes

# MAIN script
# Main basically takes the path from the command line argument and
# writes to the consol all the footnotes. 
# To save the footnotes in a file type: footnoter File > fottnotes
# To receive help write -h instad of File
if __name__ == "__main__":
    docx_file = sys.argv[1]
    if docx_file=="-h":
        # you want help, not a file!
        print("footnoter help")
        print("This command extracts all the footnotes of a .docx file")
        print("and prints them to the console")
        print("Usage: footnoter path/filename.docx")
        print("To save the footnotes to a file use the system pipes!")
        print("For example footnoter path/filename.docx > savefile.txt")
        print("Have fun!")
    else:
        footnotes = extract_footnotes(docx_file)
        if footnotes:
            for idx, footnote in enumerate(footnotes, 1):
                print(f"Footnote {idx}: {footnote}")
        else:
            print("No footnotes found.")