// MapWallpaper.tsx
import React from "react";
import { GoogleMap } from "./GoogleMap";
import "./MapWallpaper.css";

interface MapWallpaperProps {
  latitude: number;
  longitude: number;
  opacity?: number;
  blur?: string;
}

export const MapWallpaper: React.FC<MapWallpaperProps> = ({
  latitude,
  longitude,
  opacity = 0.3,
  blur = "5px",
}) => {
  return (
    <div className="map-wallpaper">
      <GoogleMap
        latitude={latitude}
        longitude={longitude}
        className="map-wallpaper__iframe"
      />
      <div
        className="map-wallpaper__overlay"
        style={{
          backgroundColor: `rgba(255, 255, 255, ${opacity})`,
          backdropFilter: `blur(${blur})`,
        }}
      ></div>
    </div>
  );
};
