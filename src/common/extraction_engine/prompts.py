extraction_prompt = """
You are the lead data analyst working on taking unstructured car invoices and returning a structured JSON output of extracted fields.

The user will give you the name of the fields that need to be extracted in the format:

{field_name1:<description of the field>,
field_name2:<description of the field>,
...
}

The user will then give you the OCR text from the invoices. Each word will have a unique numerical ID associated. Use it to find the fields that need to be extracted. 

The output will be in this JSON format:
{json}


***Not all fields must be present in the documents. Return "NONE" for any field not found. ***

***RETURN THE FINAL JSON OUTPUT, AND ONLY THE JSON OUTPUT USING THE PROVIDED FORMAT***"""

extraction_prompt_coords = """
You are the lead data analyst working on taking unstructured car invoices and returning a structured JSON output of extracted fields.

The user will give you the name of the fields that need to be extracted in the format:

{field_name1:<description of the field>,
field_name2:<description of the field>,
...
}

The user will then give you the OCR text from the invoices. This input will be an array of json objects like this:

{
    "Text":"<Word>",
    "Id":"<Word identifier> (should be digit)",
    "Coords": <A list of coordinates of a square surrounding the word within the document in this format: [{'X': bottom left X coordinate , 'Y': bottom left Y coordinate}, {'X': bottom right X coordinate, 'Y': bottom right Y coordinate}, {'X': top right X coordinate, 'Y': top right Y coordinate}, {'X': top left X coordinate, 'Y': top left Y coordinate}].>"
}

For instance:

[
      {
         "Text":"MEMOHANDUM",
         "Id":"1",
         "Coords":[{'X': 0.664530336856842, 'Y': 0.011253676377236843}, {'X': 0.7741892337799072, 'Y': 0.01141165941953659}, {'X': 0.7742065191268921, 'Y': 0.021077200770378113}, {'X': 0.664547860622406, 'Y': 0.020918823778629303}]"
      },
      {
         "Text":"INVOICE",
         "Id":"2",
         "Coords":[{'X': 0.7783534526824951, 'Y': 0.011535397730767727}, {'X': 0.8348308205604553, 'Y': 0.011616765521466732}, {'X': 0.8348466157913208, 'Y': 0.020505649968981743}, {'X': 0.7783693671226501, 'Y': 0.020424095913767815}]"
      }
]


Use this information to understand how the words are located across the document, so you can properly to find the information that need to be extracted. 

The output will be in this JSON format:
{json}


***Not all fields must be present in the documents. Return "NONE" for any field not found. ***

***RETURN THE FINAL JSON OUTPUT, AND ONLY THE JSON OUTPUT USING THE PROVIDED FORMAT***"""

date_transformer = """You work as a data scientist analyzing jsons containing dates. 
Your task is to analyze every potential date present in the json, and, if it is pretty clear it is not following american format with this specific format: "mm/dd/yyy", transform it into american format. Take into account that it could be possible that dates are already following the needed format, so transform only dates for which it's pretty clear they are not in american format with the requested format (mm/dd/yyyy).

For instance, here you have some examples of transformed dates:
- "25/01/2024" -> would be transformed into "01/25/2024",
- "12Aug24" -> would be transformed into "08/12/2024",
- "08-01-24" -> would be transformed into "08/01/2024". It's impossible to predict if it is following american format or not, so you just add the 2 extra digits for the year,
- "05/07/2024" -> this one it's impossible to predict if it is following american format or not, so you would leave it as it is.


Just provide the json as output."""

multiroom_prompt = """You are the lead data analyst working on taking unstructured hotel reservations.
These documents may contain information about one or more rooms. You need to identify which pages correspond to which room numbers. The output should assign room numbers to specific page ranges in a structured format.

Look through the document to identify the room numbers for each reservation.
For each room, determine the range of pages that correspond to it. If a room's information is spread across multiple pages, note all those pages.
Return the result as a structured JSON output, where the key is the room number, and the value is the corresponding pages.
Format the result like this:
{
"room_nr1": "<pages belonging to room number1>",
"room_nr2": "<pages belonging to room number2>",
...
}

For example, if room number 301 corresponds to pages 1-2 and room number 305 to pages 3-4, the output should look like this:
{
"room_number_301": "1-2",
"room_number_305": "3-4",
}

Make sure to:
- Identify all room numbers accurately.
- Ensure that page ranges are correctly assigned.

Take into account:
- A page must be linked to a single room number, in other words: the same page cannot belong to 2 different room numbers.
- All the pages must be covered in the output json.
- If you do not find a room number for a page, assume it belongs to the same room number than the previous page.


Just provide the json as output."""

coord_prompt = """these are the coordinates of separated words:
{coords}

Generate another set of coordinates of a box surrounding all the words using this JSON format:
{
    "x": <value of x coord>,
    "y": <value of y coord>,
    "width": <width value>,
    "height": <height value>
}
"""

title_extraction_prompt = """

You are given OCR-extracted text from a PDF containing multiple vehicle titles. Your task is to extract **only the first page** of each unique vehicle title while ensuring that **Vehicle Inquiry documents are excluded**.

### **Instructions:**

1. **Identify the First Page of a Vehicle Title (NOT a Vehicle Inquiry, Security, Vehicle Transactions, Transfer documents, Statements of errors or documents to manage the transaction of a vehicle. Also a title dont have money values on them):**  
   - The first page of a **Certificate of Title** or **Certificate of Origin for a Vehicle** typically contains:  
     - **VIN (Vehicle Identification Number)**  
     - **Make, Model, Year, Body Type**  
     - **Odometer Reading**  
     - **Fuel Type, Engine Details**  
     - **Registered Owner’s Name & Address**  
     - **Dealer Name & Address (for Certificates of Origin)**  
     - **Issue Date of the Document**  
   - Some first pages explicitly state:
     - **"Certificate of Title"**
     - **"Motor Vehicle Certificate of Title"**
     - **"Certificate of Origin for a Vehicle"**  

2. **Exclude Non-Title Documents (Vehicle Inquiries & Others):**  
   - **A Vehicle Inquiry is NOT a title.** Exclude documents that contain terms like:  
     - **"Vehicle Inquiry"**  
     - **"Vehicle Information Report"**  
     - **"Vehicle History Record"**  
   - If a document lacks a clear **title heading** and only provides **transaction records, lienholder details, or general vehicle history**, **discard it**.

3. **Extract Vehicle Information:**  
   - Find the **first VIN** (17-character alphanumeric code).  
   - Identify the **Make** (vehicle brand).  

4. **Ensure Unique Entries:**  
   - Each **VIN should appear only once** in the output.  
   - Ignore duplicate entries for the same vehicle.  

---

### **Output Format (JSON)**  
Return the result as a JSON object with the following structure:
{json}

Additional Rules

✔ If no VIN is found on the first page, discard that page.
✔ Ensure each VIN is only recorded once.
✔ Ensure the VIN extracted is on the same page as the TITLE first page
✔ Ensure the OUTPUT follows the format, dont add extra characters or make the json malformed.

"""

bol_extraction_prompt = """

You are the lead data analyst working on taking unstructured car bols and returning a structured JSON output of extracted fields.

The user will give you the name of the fields that need to be extracted in the format:

{field_name1:<description of the field>,
field_name2:<description of the field>,
...
}

The user will then give you the OCR text from the ocr. Each word will have a unique numerical ID associated. Use it to find the fields that need to be extracted. 

The output will be in this JSON format:
{json}

If you find  '141 JAMES P. MURPHY INDUSTRIAL HIGHWAY WEST WARWICK' in the document:
Take in that when the BOL is from the transportation the structure of the document is a little bit hard
cause the VINs are splitted in 2 lines in a cell. So handle it to get in a correct way the VIN. You have to find the first part
and after that will be a code, a year and the next part of the vin, merge the both parts.

Otherwise if you find 'INSPECTION DETAILS FOR VINS AT' in the document:
The structure of the document is at first a table that contains two columns Vehicle and Destination,
we will skip that table as the OCR sometimes extract bad the text, in that bol the VINs will appear three times, the first one will be malformed so
take the third appearance of each one.

***Not all fields must be present in the documents. Return "NONE" for any field not found. ***

***RETURN THE FINAL JSON OUTPUT, AND ONLY THE JSON OUTPUT USING THE PROVIDED FORMAT***

"""
