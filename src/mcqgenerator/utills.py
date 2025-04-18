import PyPDF2
import json
import traceback
import re

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_render=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_render.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("error in reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format")
    

def get_table_data(quiz_str_gemini_api):
    try:
        finalquiz_response = re.sub(r"```json|", "", quiz_str_gemini_api).strip()
        json_str_respnse= re.sub(r"```", "", finalquiz_response).strip()
        quiz_dict=json.loads(json_str_respnse)
        quiz_table_data=[]
        for item in quiz_dict:
            mcq = item["mcq"]
            options = " | ".join(
                f"{opt_key}: {opt_val}" for opt_key, opt_val in item["options"].items()
            )
            correct = item["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

