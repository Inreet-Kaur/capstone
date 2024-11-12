import { IClassifiedData } from "../models/poc";

// replaced with actual urls
const API_URL = 'localhost:8080/'; 
const TRANSCRIPTION_API_URL = 'TRANSCRIPTION_API_URL';
const CLASSIFICATION_API_URL = 'CLASSIFICATION_API_URL';

const fillClassifiedData = (rawData : Map<string, string>) => {
    const data: IClassifiedData = { 
        ...Object.fromEntries(['name', 'age', 'gender', 'insurance', 'reasonForVisit', 'symptoms', 'notes'].map(k => [k, rawData.get(k)])), 
        ...Object.fromEntries(['medicalHistory', 'allergies', 'diagnoses', 'prescriptions'].map(k => [k, rawData.get(k)?.split(',') || []])),
        labResults: [{ testName: 'Blood Glucose', result: '180 mg/dL', date: '2024-11-08' }, { testName: 'Cholesterol', result: '210 mg/dL', date: '2024-11-08' }]
    };

    return data;
}

export const getClassifiedNotes = async (audioChunk: Blob): Promise<{ 
    classifiedData: IClassifiedData; 
    transcribedText: string; 
}> => {
    console.log("Hitting");
    const sampleToken = "placeholder";
    const formData = new FormData();
    formData.append('file', audioChunk, 'recording.wav');
    
    try {
        const response = await fetch(`http://${process.env.REACT_APP_API}/${process.env.REACT_APP_API_CLFT}`, {
            method: 'POST',
            headers: {
                'x-access-token': sampleToken
            },
            body: formData
        });
        
        const data = await response.json();
        const classifiedData: IClassifiedData = fillClassifiedData(data.classified);
        return { classifiedData, transcribedText: data.transcribedText };
    } catch (error) {
        console.error('Error processing audio:', error);
        throw error;
    }
    
}


export const sendAudioService = async (audioChunk: Blob, testMode: boolean): Promise<void> => {
    if (testMode) {
        return;
    }

    const formData = new FormData();
    formData.append('audio', audioChunk, 'recording.wav');

    const response = await fetch(`${API_URL}/api/classifyText`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Failed to send audio');
    }
};

export const fetchTranscriptionService = async (testMode: boolean): Promise<string> => {
    if (testMode) {
        const mockResponses = [
            "My name is John Doe. I am 34 year old",
            "Is this you first visit?",
            "Yes this is my first visit",
            "How can I help you today",
            "I have a severe headache and nausea for the past 3 days.",
            "Also I am experiencing chest pain and shortness of breath.",
            "I see.",
            "Lets have you checked your blood sugar levels.",
            "You can collect you recogition from the reception",
            "Thanks doctor. I really like you dress btw.",
            "I was thinking to buying one in a similar stuff from suzy.",
            "Ohh really. Thank you",
            "See you next time.",
            "See you.",
            "Follow-up visit for diabetes management. Blood sugar levels stable.",
        ];
        return mockResponses[Math.floor(Math.random() * mockResponses.length)];
    }


    const response = await fetch(`${TRANSCRIPTION_API_URL}/get-transcription`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch transcription');
    }

    const data = await response.json();
    return data;
};

let callCount = 0;
export const fetchClassifiedDataService = async (testMode: boolean): Promise<IClassifiedData> => {

    if (testMode) {

        // Function to generate mock data based on call count
        const generateMockData = (): IClassifiedData => {
            callCount++;
            const mockData: IClassifiedData = {
                name: 'John Doe',
                age: '45',
                medicalHistory: ['Hypertension', 'Type 2 Diabetes'],
                ...(callCount > 1 && { gender: 'Male' }),
                ...(callCount > 2 && { insurance: 'HealthPlus Insurance, Policy #123456' }),
                ...(callCount > 3 && { reasonForVisit: 'Routine check-up' }),
                ...(callCount > 4 && { symptoms: 'Chest pain and shortness of breath, severe headache and nausea for the past 3 days' }),
                ...(callCount > 5 && { notes: 'Patient presents with flu-like symptoms including fever and body aches. Blood sugar levels high. Follow-up visit for diabetes management.' }),
                ...(callCount > 6 && {
                    allergies: ['Penicillin', 'Peanuts'],
                    diagnoses: ['High Blood Pressure', 'Diabetic Neuropathy'],
                    prescriptions: ['Lisinopril 10mg daily', 'Metformin 500mg daily'],
                    labResults: [
                        { testName: 'Blood Glucose', result: '180 mg/dL', date: '2024-11-08' },
                        { testName: 'Cholesterol', result: '210 mg/dL', date: '2024-11-08' }
                    ]
                }),
            };
            return mockData;
        };

        // Simulate async operation
        return new Promise<IClassifiedData>((resolve) => {
            setTimeout(() => {
                resolve(generateMockData());
            }, 500); // Mock async delay
        });
    }

    const response = await fetch(`${CLASSIFICATION_API_URL}/classified-data`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch additional data');
    }

    const data: IClassifiedData = await response.json();
    return data;
};


