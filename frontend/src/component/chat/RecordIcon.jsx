import React from "react";

import { ReactMediaRecorder } from "react-media-recorder-2";
import { AudioFilled } from "@ant-design/icons";

function RecordIcon({ handleStop, loader }) {
  return (
    <ReactMediaRecorder
      audio
      onStop={handleStop}
      render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
        <div>
          <button
            onMouseDown={startRecording}
            onMouseUp={stopRecording}
            class="audio-record-button"
            disabled={loader}
          >
            <div className={status === "recording"? "audio-recording audio-button" : "audio-button"}>
              <AudioFilled />
            </div>
          </button>
          <p style={{ color: "white", textAlign: "center" }}>
            {loader
              ? "Please wait"
              : status === "idle" || status === "stopped"
              ? "Hold to record"
              : status}
          </p>

          {/* <audio src={mediaBlobUrl} controls autoPlay loop /> */}
        </div>
      )}
    />
    
  );

  // return <div className='audio-button'>
  // <AudioFilled />
  // </div>
}

export default RecordIcon;
