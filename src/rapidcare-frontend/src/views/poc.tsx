import React from 'react';
import SamplePatientChart from './samplePatientChart';
import { IClassifiedData } from '../models/poc';

interface PocProps {
  isRecording: boolean;
  transcribedText: string;
  classifiedData: IClassifiedData;
  startRecording: () => void;
  stopRecording: () => void;
}

const Poc: React.FC<PocProps> = ({
  isRecording,
  transcribedText,
  classifiedData,
  startRecording,
  stopRecording,
}) => {

  return (
    <div className="flex gap-5 p-5 h-auto">
      <div className="flex-1 border border-gray-300 p-5 rounded-md">
        <div className="flex justify-center">
          <button
            onClick={isRecording ? stopRecording : startRecording}
            className={`px-5 py-2.5 ${isRecording
              ? 'bg-red-500 hover:bg-red-600'
              : 'bg-blue-500 hover:bg-blue-600'
              } text-white rounded`}
          >
            {isRecording ? 'Stop Recording' : 'Start Recording'}
          </button>
        </div>
        <div className="mt-5">
          Transcribed text will appear here.
        </div>
        <div className="mt-2 min-h-[100px] h-auto border border-black p-2.5 rounded-md">
          {transcribedText || "No transcription available"}
        </div>
      </div>

      <div className="flex-1 border border-gray-300 p-5 rounded-md">
        <SamplePatientChart patient={classifiedData} />
      </div>
    </div>
  );
};

export default Poc;

