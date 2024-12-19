import pandas as pd
import numpy as np
from typing import List, Dict, Any
from medical_processor import MedicalTextProcessor
import random
from datetime import datetime, timedelta
import json 


class MedicalDataGenerator:
    def __init__(self):
        """Initialize with expanded sample data components"""
        self.first_names = ["John", "Jane", "Ahmed", "Sarah", "Michael", "Emma", "David", "Maria", "James", "Lisa", 
                        "Robert", "Patricia", "Jennifer", "Mohammed", "Wei", "Sofia", "Amir", "Isabella", "Ethan", "Olivia"]
        
        self.last_names = ["Smith", "Johnson", "Hadary", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson",
                        "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Moore", "Taylor", "Lee"]
        
        self.symptoms = [
            "abdominal pain", "chest pain", "headache", "fever", "nausea", "vomiting", 
            "dizziness", "shortness of breath", "back pain", "joint pain",
            "muscle spasms", "difficulty walking", "cough", "sore throat", 
            "fatigue", "weakness", "anxiety", "depression", "insomnia",
            "difficulty breathing", "rash", "itching", "swelling",
            "blurred vision", "ear pain", "neck pain", "shoulder pain",
            "knee pain", "ankle pain", "numbness", "tingling",
            "loss of appetite", "weight loss", "night sweats"
        ]
        
        self.conditions = [
            "hypertension", "diabetes", "asthma", "arthritis", "anxiety", 
            "depression", "GERD", "migraine", "hypothyroidism",
            "high cholesterol", "obesity", "sleep apnea", "chronic pain",
            "fibromyalgia", "osteoporosis", "previous disc herniation",
            "coronary artery disease", "chronic kidney disease",
            "chronic bronchitis", "emphysema", "allergic rhinitis",
            "eczema", "psoriasis", "glaucoma", "cataracts"
        ]
        
        self.medications = [
            "lisinopril 10mg", "metformin 500mg", "omeprazole 20mg", "sertraline 50mg",
            "amlodipine 5mg", "levothyroxine 25mcg", "atorvastatin 40mg",
            "ibuprofen 600mg", "gabapentin 300mg", "cyclobenzaprine 10mg",
            "hydrochlorothiazide 25mg", "prednisone 5mg", "amoxicillin 500mg",
            "fluticasone nasal spray", "albuterol inhaler", "aspirin 81mg",
            "metoprolol 25mg", "furosemide 20mg", "pantoprazole 40mg",
            "tramadol 50mg", "zolpidem 5mg", "lorazepam 0.5mg","sumatriptan 50mg", 
            "propranolol 40mg"
        ]
        
        self.allergies = [
            "penicillin", "sulfa", "latex", "aspirin", "ibuprofen", 
            "shellfish", "peanuts", "eggs", "milk", "soy",
            "tree nuts", "wheat", "codeine", "morphine",
            "bees", "cats", "dogs", "dust", "mold",
            "amoxicillin", "tetracycline", "erythromycin"
        ]

    def generate_phone(self) -> str:
        return f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

    def generate_date(self) -> str:
        base = datetime.now()
        days = random.randint(0, 30)
        return (base - timedelta(days=days)).strftime("%B %d, %Y")
    
    def generate_vitals(self) -> str:
        """Generate random vitals."""
        bp = f"{random.randint(90, 140)}/{random.randint(60, 90)}"
        temp = f"{random.uniform(36.0, 38.0):.1f}"
        pulse = random.randint(60, 100)
        return f"BP: {bp}, Temp: {temp}, Pulse: {pulse}"

    def generate_lab_results(self) -> str:
        """Generate random lab results."""
        labs = ["Complete Blood Count", "X-ray Chest", "Urinalysis", "Electrolytes"]
        selected = random.sample(labs, random.randint(1, len(labs)))
        return f"Lab Results: {', '.join(selected)}"

    def generate_sample(self) -> Dict[str, Any]:
        name = f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
        age = random.randint(18, 85)
        gender = random.choice(["male", "female"])
        phone = self.generate_phone()
        main_symptom = random.choice(self.symptoms)
        extra_symptoms = random.sample(self.symptoms, random.randint(0, 2))
        vitals = self.generate_vitals()
        lab_results = self.generate_lab_results()
        allergies = random.sample(self.allergies, random.randint(0, 2))
        medical_history = random.sample(self.conditions, random.randint(1, 3))
        medications = random.sample(self.medications, random.randint(1, 3))

        template = random.choice([
            f"""NAME: {name}\nAGE: {age}\nGENDER: {gender}\nCONTACT: {phone}\nCHIEF COMPLAINT: {main_symptom}\n{vitals}\n{lab_results}\nALLERGIES: {', '.join(allergies) if allergies else 'None'}\nMEDICAL HISTORY: {', '.join(medical_history)}\nCURRENT MEDICATIONS: {', '.join(medications)}""",
            f"Patient {name} ({age} years old {gender}) arrived complaining of {main_symptom}. Contact: {phone}. {vitals} {lab_results} Allergies: {', '.join(allergies) if allergies else 'None'}. Medical history includes {', '.join(medical_history)}. Currently taking {', '.join(medications)}."
        ])

        truth = {
            "Name": name,
            "Age": age,
            "Symptoms": [main_symptom] + extra_symptoms,
            "Vitals": vitals,
            "Lab Results": lab_results.split(": ")[1].split(", "),
            "Allergies": allergies,
            "Medical History": medical_history,
            "Current Medications": medications
        }

        return {"text": template, "truth": truth}

    def generate_training_set(self, num_samples: int) -> List[Dict[str, Any]]:
        return [self.generate_sample() for _ in range(num_samples)]

# Example Usage
generator = MedicalDataGenerator()
training_data = generator.generate_training_set(50)
processor = MedicalTextProcessor()

for sample in training_data[:5]:
    print("Sample Text:", sample["text"])
    print("Extracted Name:", processor.extract_name(sample["text"]))
    print("Extracted Age:", processor.extract_age(sample["text"]))
    print("Extracted Symptoms:", processor.extract_symptoms(sample["text"]))
    print("Extracted Vitals:", processor.extract_vitals(sample["text"]))
    print("Extracted Lab Results:", processor.extract_lab_results(sample["text"]))
    print("Extracted Allergies:", processor.extract_allergies(sample["text"]))
    print("Extracted Medical History:", processor.extract_conditions(sample["text"]))
    print("Extracted Current Medications:", processor.extract_medications(sample["text"]))
    print("True Values:", sample["truth"])

# Example usage
if __name__ == "__main__":
    # Initialize generator and processor
    generator = MedicalDataGenerator()
    processor = MedicalTextProcessor()
    
    # Generate training data
    print("Generating training data...")
    training_data = generator.generate_training_set(50)  # Generate 50 samples
    
    # Prepare training texts and labels
    texts = [item["text"] for item in training_data]
    
    # Train the processor
    print("Training the processor...")
    processor.train(texts, ["medical_record"] * len(texts))
    
    # Test with your original text
    test_text = """Patient Ahmed Hadary arrived at 2:30 PM complaining of severe abdominal pain. 
    Patient is a 29 year old male with contact number 647-620-4109. Initial complaint: Severe abdominal pain and nausea.
    The pain started 2 hours ago in the lower right abdomen. Patient reports vomiting and fever as accompanying symptoms.
    Medical history includes hypertension and diabetes. Currently taking lisinopril 10mg daily and metformin 500mg twice daily. 
    Patient is allergic to penicillin and sulfa drugs."""
    
    # Process and print results
    print("\nTesting with sample text...")
    result = processor.process_text(test_text)
    
    # Print results
    print("\nExtracted Information:")
    print(json.dumps(result, indent=2))
    
    # Test with a random new format
    print("\nTesting with random new format...")
    new_sample = generator.generate_sample()
    result = processor.process_text(new_sample["text"])
    
    print("\nTrue Values:")
    print(json.dumps(new_sample["truth"], indent=2))
    print("\nExtracted Values:")
    print(json.dumps(result, indent=2))
