import { PocState } from "../models/poc";


export interface AppState {
  poc: PocState;
  //future step state
}

export const initialPocState: PocState = {
  testMode: true,
  isRecording: false,
  transcribedText: '',
  classifiedData: {
    name: '',
    age: '',
    reasonForVisit: '',
    symptoms: '',
    notes: '',
  }
};



