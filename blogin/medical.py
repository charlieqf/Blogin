import pytesseract
import spacy

### Preprocessing layer ###
# You can perform rotation and skewness correctiona, 
# colored - B/W conversion etc here

### OCR layer ###

# Perform OCR
text = pytesseract.image_to_string("medical_report.png")

print(text)
### NER layer ###

# Load the SciSpacy model
nlp = spacy.load("en_core_sci_md")

# Process the text extracted from OCR
doc = nlp(text)

### Postprocessing layer ###

# Loop through recognized entities and print canonical name
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}, Canonical Name: {ent.text}")
    