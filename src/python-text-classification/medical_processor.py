from typing import Dict, Any, List, Optional
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import json

class MedicalTextProcessor:
    def __init__(self):
        """Initialize the processor with TF-IDF vectorizer and classifier."""
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            stop_words='english'
        )
        self.classifier = RandomForestClassifier(n_estimators=100)
        
    def train(self, texts: List[str], labels: List[str]):
        """
        Train the classifier on medical texts.
        
        Args:
            texts: List of medical text samples
            labels: List of corresponding labels
        """
        # Enhance training with augmented and diverse samples
        texts, labels = self.augment_training_data(texts, labels)
        
        # Transform text to TF-IDF features
        X = self.vectorizer.fit_transform(texts)
        
        # Train the classifier
        self.classifier.fit(X, labels)
    
    def augment_training_data(self, texts: List[str], labels: List[str]) -> (List[str], List[str]):
        """Enhance training data with augmented examples."""
        augmented_texts = []
        augmented_labels = []

        for text, label in zip(texts, labels):
            # Original example
            augmented_texts.append(text)
            augmented_labels.append(label)

            # Augment with variations (e.g., synonym replacement, format changes)
            augmented_texts.append(text.replace("Patient", "Individual"))
            augmented_labels.append(label)

            augmented_texts.append(text.replace("CHIEF COMPLAINT", "Main Issue"))
            augmented_labels.append(label)

        return texts + augmented_texts, labels + augmented_labels

    def classify_section(self, text: str) -> str:
        """Classify a piece of text into predefined categories."""
        X = self.vectorizer.transform([text])
        return self.classifier.predict(X)[0]

    def extract_name(self, text: str) -> str:
        """Enhanced regex to extract patient name."""
        patterns = [
            # Match structured format with NAME: prefix
            r"(?:NAME|Patient Name):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:\s*\n|\s*$|\s*,)",
            
            # Match "Patient [Name]" at start of sentence
            r"Patient\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?=\s+(?:arrived|is|was|presents|complains|reports))",
            
            # Match name with age indicator
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?=\s*(?:\(|\s+is\s+)?\d{1,3}\s*(?:year|yo|y\.o\.|years))",
            
            # Match structured name at start of line
            r"(?:^|\n)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:\n|,|\s+(?:is|was|arrived|presents|complains|reports))"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                # Clean up any trailing whitespace or newlines
                return match.group(1).strip()
        
        return None

    def extract_symptoms(self, text: str) -> List[str]:
        """Enhanced regex to extract symptoms with more patterns."""
        patterns = [
            r"(?:CHIEF COMPLAINT|SYMPTOMS|complaint|Main Issue):\s*(.*?)(?:\.|$|\n)",
            r"(?:presents with|complaining of)\s*(.*?)(?:\.|$|\n)",
            r"(?:Additional )?Symptoms?:\s*(.*?)(?:\.|$|\n)",
            r"(productive cough[^.]*)",
            r"((?:fever|fatigue|sputum)[^.]*)"
        ]
        symptoms = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                text_to_process = next((g for g in groups if g is not None), match.group(0))
                # Split on multiple delimiters and clean each symptom
                symptoms.extend([s.strip() for s in re.split(r',|\sand\s|;\s*', text_to_process) 
                            if s.strip() and not s.lower().startswith(('patient', 'presents', 'complaining'))])
        
        return list(set(symptoms))  # Remove duplicates

    def extract_medications(self, text: str) -> List[str]:
        """Enhanced regex to extract current medications."""
        medications = []
        patterns = [
            r"(?:CURRENT MEDICATIONS|MEDICATIONS|Medications|Meds):\s*(.*?)(?:\.|$|\n)",
            r"(?:currently taking|using)\s+(.*?)(?:\.|$|\n)",
            r"Meds:\s*(.*?)(?:\.|$|\n)",
            r"(?:Ventolin|Flonase)[^.]*"
        ]
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                text_to_process = next((g for g in groups if g is not None), match.group(0))
                meds = re.split(r',|\sand\s', text_to_process)
                medications.extend([m.strip() for m in meds if m.strip()])
        return list(set(medications))

    def extract_conditions(self, text: str) -> List[str]:
        """Enhanced regex to extract medical history/conditions."""
        conditions = []
        patterns = [
            r"(?:MEDICAL HISTORY|Past Medical History|PMH):\s*(.*?)(?:\.|$|\n)",
            r"history includes\s+(.*?)(?:\.|$|\n)",
            r"diagnosed with\s+(.*?)(?:\.|$|\n)",
            r"PMH:\s*(.*?)(?:\.|$|\n)"
        ]
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                text_to_process = next((g for g in groups if g is not None), match.group(0))
                conditions.extend([c.strip() for c in re.split(r',|\sand\s', text_to_process)
                                if c.strip()])
        
        # Also look for specific conditions
        specific_conditions = [
            r"(?:smoker|seasonal allerg(?:y|ies))"
        ]
        for pattern in specific_conditions:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                conditions.append(match.group(0))
        
        return list(set(conditions))

    def extract_allergies(self, text: str) -> List[str]:
        """Enhanced method to extract allergies from text."""
        allergy_patterns = [
            r"(?:ALLERGIES|Allergies|Known Allergies):\s*(.*?)(?:\.|$|\n)",
            r"(?:allergic to)\s+(.*?)(?:\.|$|\n)",
            r"(?:Known Allergies|Known Allergies:)\s*(.*?)(?:\.|$|\n)",
            r"(?:PCN|NKDA)"
        ]
        
        extracted_allergies = set()
        
        # First check for explicit "none" patterns
        none_patterns = [
            r"(?:ALLERGIES|Allergies|Known Allergies):\s*(?:None|NKDA|no known drug allergies|no known allergies)",
            r"(?:NKDA|no known drug allergies|no known allergies)"
        ]
        
        for pattern in none_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return ["None"]
        
        # Then look for actual allergies
        for pattern in allergy_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                allergy_text = match.group(1).strip() if match.group(1) else match.group(0).strip()
                allergies = re.split(r',|\sand\s', allergy_text)
                extracted_allergies.update([a.strip() for a in allergies if a.strip()])
        
        return list(extracted_allergies) if extracted_allergies else ["None"]
    def extract_lab_results(self, text: str) -> List[str]:
        """Enhanced regex to extract lab results."""
        results = []
        patterns = [
            r"(?:Lab Results|Labs|Tests|LABS ORDERED):\s*(.*?)(?:\.|$)",
            r"(?:Tests Ordered):\s*(.*?)(?:\.|$)",
            r"Tests:\s*(.*?)(?:\.|$)",
            r"(?:Rapid strep|CXR)[^.]*"
        ]
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get all captured groups and use the first non-None group
                groups = match.groups()
                text_to_process = next((g for g in groups if g is not None), match.group(0))
                results.extend(re.split(r",\s*|\s+and\s+", text_to_process))
        
        return [result.strip() for result in results if result.strip() and not result.lower().startswith('test')]

    def extract_vitals(self, text: str) -> Dict[str, str]:
        """Enhanced regex to extract vitals."""
        vitals = {}
        patterns = {
            "BP": r"(?:BP|Blood Pressure):?\s*(\d{2,3}/\d{2,3})",
            "Temp": r"(?:Temp|Temperature|T):?\s*(\d{2,3}(?:\.\d+)?)",
            "Pulse": r"(?:Pulse|Heart Rate|HR|P):?\s*(\d{2,3})",
            "RR": r"(?:RR|Respiratory Rate):?\s*(\d{1,2})",
            "O2": r"O2\s*(?:sat|saturation)?\s*(?:is|of)?\s*(\d{1,3}%)"
        }
        
        # First look for vitals section
        vital_sections = re.finditer(r"(?:VS|Vitals|Vital signs):[^.]*", text, re.IGNORECASE)
        for section in vital_sections:
            section_text = section.group(0)
            for key, pattern in patterns.items():
                match = re.search(pattern, section_text, re.IGNORECASE)
                if match:
                    vitals[key] = match.group(1)
        
        # Then look for vitals in the entire text
        for key, pattern in patterns.items():
            if key not in vitals:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    vitals[key] = match.group(1)
        
        # Clean up temperature if found
        if 'Temp' in vitals:
            temp = float(vitals['Temp'])
            if temp > 45:  # Probably Fahrenheit
                temp = round((temp - 32) * 5/9, 1)
            vitals['Temp'] = str(temp)
        
        return vitals

    def extract_age(self, text: str) -> int:
        """Enhanced regex to extract patient age."""
        patterns = [
            r"(\d{1,3})\s*(?:year[s]?\s*old|yo|y\.o\.?)",
            r"age:?\s*(\d{1,3})",
            r"\((\d{1,3})\s*(?:yo|year)"
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def extract_gender(self, text: str) -> Optional[str]:
        """Extract patient gender."""
        male_patterns = [r'\bmale\b', r'\bM\b', r'gentleman', r'sir']
        female_patterns = [r'\bfemale\b', r'\bF\b', r'lady', r'madam']
        
        text_lower = text.lower()
        
        for pattern in male_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "Male"
                
        for pattern in female_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "Female"
                
        return None

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information including phone and email."""
        contact_info = {}
        
        # Phone patterns
        phone_patterns = [
            r"(?:Phone|Contact|TEL|phone|contact|tel)(?:\s*(?:number|#))?:?\s*(\d{3}[-.]?\d{3}[-.]?\d{4})",
            r"(\d{3}[-.]?\d{3}[-.]?\d{4})",  # Standard phone
            r"(\+\d{1,3}[-.]?\d{3}[-.]?\d{3}[-.]?\d{4})"  # International
        ]
        
        # Email pattern
        email_pattern = r"(?:Email|email|e-mail):\s*([\w\.-]+@[\w\.-]+\.\w+)|[\w\.-]+@[\w\.-]+\.\w+"
        
        # Extract phone
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                contact_info['phone'] = match.group(1)
                break
                
        # Extract email
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group(1) if email_match.group(1) else email_match.group(0)
            
        return contact_info

    def extract_medical_info(self, text: str) -> Dict[str, List[str]]:
        """Extract various medical information using regex patterns."""
        medical_info = {
            'symptoms': self.extract_symptoms(text),
            'conditions': self.extract_conditions(text),
            'medications': self.extract_medications(text),
            'allergies': self.extract_allergies(text),
            'vitals': self.extract_vitals(text),
            'lab_results': self.extract_lab_results(text)
        }
        
        return medical_info

    def process_text(self, text: str) -> Dict[str, Any]:
        """Process medical text and return structured data."""
        # Extract all information
        medical_info = self.extract_medical_info(text)
        
        return {
            "Name": self.extract_name(text),
            "Age": self.extract_age(text),
            "Gender": self.extract_gender(text),
            "Contact-Info": self.extract_contact_info(text),
            "Reason For Visit": medical_info['symptoms'][0] if medical_info['symptoms'] else None,
            "Symptoms": medical_info['symptoms'],
            "Notes": text,
            "Medical History": medical_info['conditions'],
            "Allergies": medical_info['allergies'],
            "Current Medications": medical_info['medications'],
            "Vitals": medical_info['vitals'],
            "Lab Results": medical_info['lab_results']
        }

# Example usage
if __name__ == "__main__":
    # Comprehensive training data covering different medical record aspects
    sample_texts = [
        # Symptoms
        "Patient presents with fever and cough",
        "Patient reports severe headache with photophobia",
        "Chief complaint: shortness of breath and chest pain",
        "Patient experiencing nausea and abdominal pain",
        
        # Medical History
        "History of diabetes and hypertension",
        "Past medical history includes asthma and GERD",
        "Previously diagnosed with rheumatoid arthritis",
        "History of myocardial infarction in 2020",
        
        # Medications
        "Currently taking metformin 500mg twice daily",
        "Medications include lisinopril 10mg and aspirin 81mg",
        "Patient uses albuterol inhaler as needed",
        "Taking levothyroxine 75mcg every morning",
        
        # Allergies
        "Patient is allergic to penicillin and sulfa drugs",
        "Known allergies: latex, shellfish",
        "NKDA (No Known Drug Allergies)",
        "Allergic to ibuprofen - causes rash",
        
        # Vitals
        "BP 140/90, Temperature 38.2C, HR 88",
        "Vital signs: Blood pressure 122/78, Pulse 72",
        "Temperature 37.5, oxygen saturation 98%",
        
        # Lab Results
        "Lab results show elevated white blood cell count",
        "Recent A1C: 7.2, Basic metabolic panel normal",
        "Pending CBC and lipid panel"
    ]
    
    sample_labels = [
        # Labels for symptoms
        "symptoms", "symptoms", "symptoms", "symptoms",
        
        # Labels for medical history
        "medical_history", "medical_history", "medical_history", "medical_history",
        
        # Labels for medications
        "medications", "medications", "medications", "medications",
        
        # Labels for allergies
        "allergies", "allergies", "allergies", "allergies",
        
        # Labels for vitals
        "vitals", "vitals", "vitals",
        
        # Labels for lab results
        "lab_results", "lab_results", "lab_results"
    ]
    
    # Initialize and train
    processor = MedicalTextProcessor()
    print("Training model with sample data...")
    processor.train(sample_texts, sample_labels)
    
    # Test cases with different formats
    test_cases = [
        # Standard narrative format
        """Patient Ahmed Hadary arrived at 2:30 PM complaining of severe abdominal pain. 
        Patient is a 29 year old male with contact number 647-620-4109. Initial complaint: Severe abdominal pain and nausea.
        The pain started 2 hours ago in the lower right abdomen. Patient reports vomiting and fever as accompanying symptoms.
        Medical history includes hypertension and diabetes. Currently taking lisinopril 10mg daily and metformin 500mg twice daily. 
        Patient is allergic to penicillin and sulfa drugs.
        Vitals: BP 130/85, Temp 38.1, HR 88""",
        
        # Structured format with headers
        """NAME: Emily Johnson
        AGE: 45
        GENDER: Female
        CONTACT: 416-555-7890
        EMAIL: emily.j@email.com
        
        CHIEF COMPLAINT: Migraine headache
        SYMPTOMS: Photophobia, nausea, visual aura
        ONSET: Started 6 hours ago
        
        MEDICAL HISTORY: Chronic migraines, hypothyroidism
        CURRENT MEDICATIONS: Sumatriptan 50mg PRN, levothyroxine 75mcg daily
        ALLERGIES: None
        
        VITALS:
        BP: 120/80
        Temp: 36.8
        HR: 72
        
        LABS ORDERED: TSH, CBC""",
        
    ]
    
    # Process and evaluate each test case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nProcessing Test Case #{i}")
        print("=" * 50)
        
        result = processor.process_text(test_case)
        
        print("\nExtracted Information:")
        print(json.dumps(result, indent=2))
        
        # Validation summary
        fields_present = sum(1 for v in result.values() if v is not None and v != [] and v != {})
        print(f"\nFields Extracted: {fields_present}/{len(result)}")
        
        print("\nMissing Fields:")
        missing_fields = []
        for field, value in result.items():
            if value is None or value == [] or value == {}:
                missing_fields.append(field)
                print(f"- {field}")
        
        if not missing_fields:
            print("No missing fields!")