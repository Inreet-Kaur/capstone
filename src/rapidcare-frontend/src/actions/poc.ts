import { Dispatch } from 'redux';
import { fetchClassifiedDataService, fetchTranscriptionService, sendAudioService } from '../services/pocService';
import { AppState } from '../reducers/AppState';
import { IClassifiedData } from '../models/poc';

export const SET_TRANSCRIBED_TEXT = 'SET_TRANSCRIBED_TEXT';
export const SET_CLASSIFIED_DATA = 'SET_CLASSIFIED_DATA';
// export const START_RECORDING = 'START_RECORDING';
// export const STOP_RECORDING = 'STOP_RECORDING';

export const sendAudio = (audioChunk: Blob) => async (dispatch: Dispatch, getState: () => AppState) => {
    const { testMode } = getState().poc;
    try {
        await sendAudioService(audioChunk, Boolean(testMode));
    } catch (error) {
        console.error('Error sending audio:', error);
    }
};

export const fetchTranscribedText = () => async (dispatch: Dispatch, getState: () => AppState) => {
    const { testMode } = getState().poc;
    try {
        const transcribedText = await fetchTranscriptionService(Boolean(testMode));
        dispatch({
            type: SET_TRANSCRIBED_TEXT,
            payload: transcribedText,
        });
    } catch (error) {
        console.error('Error fetching transcription:', error);
    }
};

export const fetchClassifiedData = () => async (dispatch: Dispatch, getState: () => AppState) => {
    const { testMode } = getState().poc;
    try {
        const data: IClassifiedData = await fetchClassifiedDataService(Boolean(testMode));
        dispatch({
            type: SET_CLASSIFIED_DATA,
            payload: data,
        });
    } catch (error) {
        console.error('Error fetching classified data:', error);
    }
};

// // Action to stop recording
// export const startRecording = () => ({
//     type: STOP_RECORDING,
// });

// // Action to stop recording
// export const stopRecording = () => ({
//     type: STOP_RECORDING,
// });
