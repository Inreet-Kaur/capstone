from train import MedicalDataGenerator
from medical_processor import MedicalTextProcessor
import json

def main():
    # Create instances
    print("Initializing...")
    generator = MedicalDataGenerator()
    processor = MedicalTextProcessor()

    # Generate and train with 1000 samples instead of 500
    print("Generating training data...")
    training_data = generator.generate_training_set(1000)
    texts = [item["text"] for item in training_data]
    
    print("Training the model...")
    processor.train(texts, ["medical_record"] * len(texts))

    # Test texts in different formats
    test_texts = [
        """
        Patient James Wilson arrived at 10:15 AM complaining of severe chest pain. 
        Patient is a 45 year old male with contact number 416-555-0123. 
        Initial complaint: Chest pain and shortness of breath.
        The pain started 1 hour ago and radiates to the left arm. Patient reports sweating and nausea as accompanying symptoms.
        Medical history includes high cholesterol and anxiety. Currently taking atorvastatin 40mg daily and sertraline 50mg daily. 
        Patient is allergic to aspirin and shellfish.
        BP: 140/90, Temp: 37.2, Pulse: 95
        """,

        """
        NAME: Sarah Brown
        AGE: 32
        GENDER: Female
        CONTACT: 647-555-8900
        CHIEF COMPLAINT: Migraine headache
        ADDITIONAL SYMPTOMS: Sensitivity to light, nausea, dizziness
        MEDICAL HISTORY: Chronic migraines, depression
        CURRENT MEDICATIONS: sumatriptan 50mg, propranolol 40mg
        ALLERGIES: None
        VITALS: BP 120/80, Temp 36.8
        """
    ]

    # Process each test text
    for i, test_text in enumerate(test_texts, 1):
        print(f"\nProcessing test text #{i}...")
        result = processor.process_text(test_text)
        print(f"\nResults for test #{i}:")
        print(json.dumps(result, indent=2))
        print("\n" + "="*50)

if __name__ == "__main__":
    main()