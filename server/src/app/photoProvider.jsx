/* eslint-disable react/prop-types */
import React, { createContext, useEffect, useState } from 'react'
import api from './api'

export const PhotoContext = createContext(null)

export default function PhotoProvider ({ children }) {
  const [gallery, setGallery] = useState([])
  const [photo, setPhoto] = useState(null)

  const store = {
    gallery: [gallery, setGallery],
    photo: [photo, setPhoto]
  }

  useEffect(() => {
    api.metadata()
      .then((data) => setGallery(data))
      .catch((error) => console.error(error))
  }, [])

  return (
    <PhotoContext.Provider value={store}>
      {children}
    </PhotoContext.Provider>
  )
}
