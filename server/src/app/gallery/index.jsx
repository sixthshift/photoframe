import React, { useContext } from 'react'
import PhotoAlbum from 'react-photo-album'

import { PhotoContext } from '../photoProvider'
import Editor from '../editor'

export default function Gallery () {
  const {
    gallery: [gallery],
    photo: [, setPhoto]
  } = useContext(PhotoContext)

  return (
    <>
      <PhotoAlbum
        layout="masonry"
        photos={gallery}
        onClick={({ photo }) => {
          setPhoto(photo)
        }}
        spacing={5}
      />
      <Editor />
    </>
  )
}
