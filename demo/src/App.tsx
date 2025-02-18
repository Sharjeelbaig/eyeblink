import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { firestore } from "./firebase";
import { collection, getDocs } from "firebase/firestore";

export default function App() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [ear, setEar] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [imageBase64, setImageBase64] = useState<string | null>(null);
  const [user, setUser] = useState<string | null>(null);

  useEffect(() => {
    if (isStreaming) {
      const interval = setInterval(sendFrame, 500);
      return () => clearInterval(interval);
    }
  }, [isStreaming]);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    if (videoRef.current) videoRef.current.srcObject = stream;
    // set stream true if the camera is on
    if (stream) setIsStreaming(true);
  };

  const stopCamera = () => {
    const stream = videoRef.current?.srcObject as MediaStream;
    stream?.getTracks().forEach((track) => track.stop());
    // set stream false if the camera is off
    setIsStreaming(false);
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
    setImageBase64(imageBase64);
  };

  const getEAR = async (imageBase64: string) => {
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

  const verifyUser = async (imageBase64: string) => {
    const querySnapshot = await getDocs(collection(firestore, "Users"));
    querySnapshot.forEach(async (doc: any) => {
      if (!doc.data().base64) return;
      let data = JSON.stringify({
        image1: doc.data().base64,
        image2: imageBase64,
      });
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: "http://localhost:5001/compare",
        headers: {
          "Content-Type": "text/plain",
          "content-type": "application/json",
        },
        data: data,
      };
      await axios
        .request(config)
        .then((response) => {
          if (response.data === "OK") {
            setUser(doc.data().name);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    });
  };

  useEffect(() => {
    if (imageBase64) {
      getEAR(imageBase64)?.then(() => {});
    }
  }, [imageBase64]);

  useEffect(() => {
    // recognize the user if the user is null
    if (isStreaming) {
      if (!user) {
        verifyUser(imageBase64 ?? "");
      }
    }
  }, [user, isStreaming]);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>User: {user ?? "N/A"}</h1>
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
          }}
        >
          Start
        </button>
        <button
          onClick={() => {
            stopCamera();
          }}
        >
          Stop
        </button>
        <button
          onClick={() => {
            if (imageBase64) verifyUser(imageBase64);
          }}
        >
          Verify User
        </button>
      </div>
    </div>
  );
}
