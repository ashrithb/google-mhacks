import React, { StrictMode, useState, useEffect } from "react";
import { createRoot } from "react-dom/client";

export default function Image({ imageURL }) {
    return <img src={imageURL} alt="Description" />;
}