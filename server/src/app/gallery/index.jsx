import React, { useContext } from 'react'
import PhotoAlbum from 'react-photo-album'

import { PhotoContext } from '../photos'
import RenderPhoto from './renderPhoto'

export default function Gallery () {
  const [photos] = useContext(PhotoContext)
  return (
      <PhotoAlbum
        layout="masonry"
        photos={photos}
        // renderPhoto={RenderPhoto}
      />
  )
}
