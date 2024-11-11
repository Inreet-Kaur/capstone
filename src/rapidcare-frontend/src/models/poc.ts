export interface PocState {
    testMode: Boolean;
    isRecording: Boolean;
    transcribedText: string;
    classifiedData: IClassifiedData;
  }
  
  export interface IClassifiedData {
    name?: string;
    age?: string;
    gender?: string;
    contactInfo?: string;
    insurance?: string;
    reasonForVisit?: string;
    symptoms?: string,
    notes?: string
    medicalHistory?: string[];
    allergies?: string[];
    diagnoses?: string[];
    prescriptions?: string[];
    labResults?: ILabResult[];
  }
  
  export interface ILabResult {
    testName?: string;
    result?: string;
    date?: string;
  };