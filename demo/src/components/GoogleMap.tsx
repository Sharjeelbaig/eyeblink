// GoogleMap.tsx
import React from "react";
import "./GoogleMap.css";

interface GoogleMapProps {
  latitude: number;
  longitude: number;
  width?: string;
  height?: string;
  className?: string;
}

export const GoogleMap: React.FC<GoogleMapProps> = ({
  latitude,
  longitude,
  width = "100%",
  height = "100%",
  className = "",
}) => {
  const mapSrc = `https://maps.google.com/maps?width=${width}&height=${height}&hl=en&q=${latitude},${longitude}&t=&z=14&ie=UTF8&iwloc=B&output=embed`;

  return (
    <iframe
      className={`gmap_iframe ${className}`}
      frameBorder="0"
      scrolling="no"
      marginHeight={0}
      marginWidth={0}
      src={mapSrc}
      allowFullScreen
      style={{ scale: 1.4 }}
    ></iframe>
  );
};
