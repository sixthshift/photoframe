/* eslint-disable react/prop-types */
import React, { createContext, useEffect, useState } from 'react'

export const PhotoContext = createContext(null)

export default function PhotoProvider ({ children }) {
  const [photos, setPhotos] = useState([])

  useEffect(() => {
    fetch('metadata')
      .then((response) => response.json())
      .then((data) => setPhotos(data))
      .catch((error) => console.error(error))
  }, [])

  return (
    <PhotoContext.Provider value={[photos, setPhotos]}>
      {children}
    </PhotoContext.Provider>
  )
}
