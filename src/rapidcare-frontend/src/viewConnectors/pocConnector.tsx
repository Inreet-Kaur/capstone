import { connect } from 'react-redux';
import { sendAudio, fetchTranscribedText, fetchClassifiedData } from '../actions/poc';
import Poc from '../views/poc';
import { AppState } from '../reducers/AppState';
import { useState, useEffect } from 'react';

const POLLING_INTERVAL = 1000;

interface StateProps {
  transcribedText: string;
  classifiedData: any;
}

interface DispatchProps {
  sendAudio: (audioData: Blob) => void;
  fetchTranscribedText: () => void;
  fetchClassifiedData: () => void;
}

interface PocConnectorProps extends StateProps, DispatchProps { }

const mapStateToProps = (state: AppState): StateProps => ({
  transcribedText: state.poc.transcribedText,
  classifiedData: state.poc.classifiedData,
});

const mapDispatchToProps: DispatchProps = {
  sendAudio,
  fetchTranscribedText,
  fetchClassifiedData,
};

const Connector = (props: PocConnectorProps) => {
  const { sendAudio, fetchTranscribedText, fetchClassifiedData } = props;
  const [isRecording, setIsRecording] = useState(false);
  const [isPolling, setIsPolling] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const audioChunks: BlobPart[] = [];

  useEffect(() => {
    let fetchInterval: NodeJS.Timeout;
    if (isPolling) {
      fetchInterval = setInterval(() => {
        Promise.all([
          fetchTranscribedText(),
          fetchClassifiedData()
        ]).catch(console.error);
      }, POLLING_INTERVAL);
    }
    return () => clearInterval(fetchInterval);
  }, [isPolling, fetchTranscribedText, fetchClassifiedData]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);

      recorder.ondataavailable = (event: BlobEvent) => {
        audioChunks.push(event.data);
        sendAudio(event.data);
      };

      recorder.onstop = () => {
        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start(1000);
      setIsRecording(true);
      setTimeout(() => setIsPolling(true), 1000);
    } catch (error) {
      console.error("Error accessing microphone", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
      setTimeout(() => setIsPolling(false), 2000);
    }
  };

  return (
    <Poc
      isRecording={isRecording}
      transcribedText={props.transcribedText}
      classifiedData={props.classifiedData}
      startRecording={startRecording}
      stopRecording={stopRecording}
    />
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(Connector);

