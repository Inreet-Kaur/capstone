import { SET_TRANSCRIBED_TEXT, SET_CLASSIFIED_DATA } from '../actions/poc';
import { PocState } from '../models/poc';
import { initialPocState } from './AppState';

const pocReducer = (state = initialPocState, action: any): PocState => {
  switch (action.type) {

    case SET_TRANSCRIBED_TEXT:
      return {
        ...state,
        transcribedText: state.transcribedText + action.payload,
      };

    case SET_CLASSIFIED_DATA:
      return {
        ...state,
        classifiedData: action.payload,
      };

    // case START_RECORDING:
    //   return {
    //     ...state,
    //     isRecording: true,
    //   };

    // case STOP_RECORDING:
    //   return {
    //     ...state,
    //     isRecording: false,
    //   };

    default:
      return state;
  }
};

export default pocReducer;
