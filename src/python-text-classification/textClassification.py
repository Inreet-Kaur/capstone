from typing import Dict, List, Optional
import re
import spacy
from datetime import datetime

class TriageTextClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Modified keywords to match new interface
        self.field_keywords = {
            "SYMPTOMS": ["pain", "ache", "discomfort", "feeling", "nausea", "vomiting", "fever"],
            "MEDICAL_HISTORY": ["history", "diagnosed", "chronic", "condition", "previous"],
            "ALLERGIES": ["allergic", "allergy", "allergies", "reaction", "sensitive"],
            "DIAGNOSES": ["diagnosed with", "assessment", "impression", "conclusion"],
            "PRESCRIPTIONS": ["prescribed", "medication", "take", "dose", "medicine"],
            "REASON": ["reason for visit", "complaint", "presenting with", "here for"],
            "CONTACT": ["phone", "contact", "email", "address", "reach"],
            "INSURANCE": ["insurance", "coverage", "policy", "insured"]
        }

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize the input text."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_name(self, text: str) -> Optional[str]:
        name_pattern = r'Patient\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,2})'
        match = re.search(name_pattern, text)
        return match.group(1) if match else None

    def extract_age(self, text: str) -> Optional[str]:
        """Extract age from text using multiple patterns."""
        # Direct age patterns
        age_patterns = [
            r'(\d+)[-\s]*year[-\s]*old',  # matches "45 year old", "45-year-old"
            r'(\d+)\s*(?:y/?o)',          # matches "45 y/o", "45yo"
            r'age(?:d)?\s*:?\s*(\d+)',    # matches "age: 45", "aged 45"
            r'(\d+)[-\s]*years?\s*of\s*age', # matches "45 years of age"
        ]
        
        # First try to find direct age mentions
        for pattern in age_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # If no direct age found, look for combined patterns like "45-year-old male"
        combined_pattern = r'(?:is\s+)?(?:a\s+)?(\d+)[-\s]*year[-\s]*old\s*(?:male|female|patient|person)?'
        match = re.search(combined_pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
                
        # As a fallback, try to calculate age from birth year
        birth_pattern = r'born\s+(?:on\s+)?(?:[A-Za-z]+\s+\d{1,2},?\s+)?(\d{4})'
        match = re.search(birth_pattern, text, re.IGNORECASE)
        if match:
            birth_year = int(match.group(1))
            current_year = datetime.now().year
            return str(current_year - birth_year)
            
        return None

    def extract_gender(self, text: str) -> Optional[str]:
        gender_pattern = r'\b(male|female)\b'
        match = re.search(gender_pattern, text, re.IGNORECASE)
        return match.group(1).capitalize() if match else None

    def extract_contact_info(self, text: str) -> Optional[str]:
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None

    def extract_reason_for_visit(self, text: str) -> Optional[str]:
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.field_keywords["REASON"]):
                return sentence.strip()
        return None

    def extract_symptoms(self, text: str) -> Optional[str]:
        symptoms = []
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.field_keywords["SYMPTOMS"]):
                symptoms.append(sentence.strip())
        return '; '.join(symptoms) if symptoms else None

    def extract_medical_history(self, text: str) -> List[str]:
        history = []
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.field_keywords["MEDICAL_HISTORY"]):
                history.append(sentence.strip())
        return history

    def extract_allergies(self, text: str) -> List[str]:
        allergies = []
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.field_keywords["ALLERGIES"]):
                allergies.append(sentence.strip())
        return allergies

    def extract_diagnoses(self, text: str) -> List[str]:
        diagnoses = []
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.field_keywords["DIAGNOSES"]):
                diagnoses.append(sentence.strip())
        return diagnoses

    def extract_prescriptions(self, text: str) -> List[str]:
        prescriptions = []
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.field_keywords["PRESCRIPTIONS"]):
                prescriptions.append(sentence.strip())
        return prescriptions

    def extract_lab_results(self, text: str) -> List[Dict[str, str]]:
        lab_results = []
        lab_pattern = r'(CBC|CMP|lipase|blood\s+work|test)'
        dates_pattern = r'(?:on|dated?)\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})'
        
        sentences = text.split('.')
        for sentence in sentences:
            test_match = re.search(lab_pattern, sentence, re.IGNORECASE)
            date_match = re.search(dates_pattern, sentence, re.IGNORECASE)
            
            if test_match:
                result = {
                    "testName": test_match.group(1),
                    "result": "Pending",  # Default to pending if no result specified
                    "date": date_match.group(1) if date_match else datetime.now().strftime('%B %d, %Y')
                }
                lab_results.append(result)
        
        return lab_results

    def classify_text(self, text: str) -> Dict:
        """Classify text into the IClassifiedData structure."""
        processed_text = self.preprocess_text(text)
        
        classified_data = {
            "Name": self.extract_name(processed_text),
            "Age": self.extract_age(processed_text),
            "Gender": self.extract_gender(processed_text),
            "Contact-Info": self.extract_contact_info(processed_text),
            "Insurance": None,  # Add insurance extraction if needed
            "Reason For Visit": self.extract_reason_for_visit(processed_text),
            "Symptoms": self.extract_symptoms(processed_text),
            "Notes": processed_text,  # Store full text as notes
            "Medical History": self.extract_medical_history(processed_text),
            "Allergies": self.extract_allergies(processed_text),
            "Diagnoses": self.extract_diagnoses(processed_text),
            "Prescriptions": self.extract_prescriptions(processed_text),
            "Lab Results": self.extract_lab_results(processed_text)
        }
        
        # Remove None values to match TypeScript optional fields
        return {k: v for k, v in classified_data.items() if v is not None}

def example_usage():
    sample_text = """
    Patient Ahmed Hadary arrived at 2:30 PM complaining of severe abdominal pain.
    Patient is a 29 year old male with contact number 647-620-4109.
    Initial complaint: Severe abdominal pain and nausea.
    
    The pain started 2 hours ago in the lower right abdomen.
    Patient reports vomiting and fever as accompanying symptoms.
    
    Medical history includes hypertension and diabetes.
    Currently taking lisinopril 10mg daily and metformin 500mg twice daily.
    Patient is allergic to penicillin and sulfa drugs.
    
    Initial assessment suggests possible appendicitis.
    Prescribed Zofran 4mg IV for nausea.
    
    CMP tests ordered on November 10, 2024.
    """
    
    classifier = TriageTextClassifier()
    classified_data = classifier.classify_text(sample_text)
    
    # Print results in a formatted way
    for field, value in classified_data.items():
        print(f"\n{field}:")
        print(value)

if __name__ == "__main__":
    example_usage()