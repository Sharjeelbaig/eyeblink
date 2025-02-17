import { useEffect, useRef, useState } from "react";
import axios from "axios";

export default function App() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [ear, setEar] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    if (isStreaming) {
      const interval = setInterval(sendFrame, 500);
      return () => clearInterval(interval);
    }
  }, [isStreaming]);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    if (videoRef.current) videoRef.current.srcObject = stream;
  };

  const stopCamera = () => {
    const stream = videoRef.current?.srcObject as MediaStream;
    stream?.getTracks().forEach((track) => track.stop());
  };

  const sendFrame = async () => {
    if (!videoRef.current) return;
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    if (!context) return;
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    context.drawImage(videoRef.current, 0, 0);
    const imageBase64 = canvas.toDataURL("image/jpeg").split(",")[1];
    console.log(imageBase64);

    let data = JSON.stringify({
      image: imageBase64,
    });

    let config = {
      method: "post",
      maxBodyLength: Infinity,
      url: "http://localhost:5001/ear",
      headers: {
        "Content-Type": "application/json",
      },
      data: data,
    };

    axios
      .request(config)
      .then((response) => {
        console.log(JSON.stringify(response.data));
        setEar(response.data.ear.toFixed(4));
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        style={{ width: "100%", borderRadius: "8px" }}
      />
      <h1>{parseFloat(ear ?? "0") < 0.2 ? "Drowsiness" : ""}</h1>
      <h3>EAR: {ear ?? "N/A"}</h3>
      <h6>
        Eye Aspect Ratio (EAR) is a measure of the eye openness. A lower EAR
        value indicates the eyes are closed or almost
      </h6>
      <div>
        <button
          onClick={() => {
            startCamera();
            setIsStreaming(true);
          }}
        >
          Start
        </button>
        <button
          onClick={() => {
            stopCamera();
            setIsStreaming(false);
          }}
        >
          Stop
        </button>
      </div>
    </div>
  );
}
