import React, { useContext, useRef } from 'react'
import { Button } from 'react-bootstrap'

import { PhotoContext } from '../photoProvider'
import api from '../api'

const isValidPhoto = (file) => {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader()
    fileReader.readAsDataURL(file)
    fileReader.onload = (event) => {
      const image = new Image()
      image.src = event.target.result
      image.onload = () => {
        resolve(file)
      }
      image.onerror = () => {
        reject(new Error('Not a valid image'))
      }
    }
  })
}

export default function Upload () {
  const [, setGallery] = useContext(PhotoContext).gallery
  const fileInput = useRef(null)

  const onUpload = (event) => {
    Array.from(event.target.files).forEach((file) => {
      isValidPhoto(file)
        .then(api.upload)
        .then(setGallery)
        .catch((err) => { console.error(err) })
    })
    fileInput.current.value = ''
  }

  return (
    <div>
      <input id="upload" type="file" className='d-none' multiple
        ref={fileInput}
        onChange={onUpload}
      />
      <label htmlFor="upload">
        <Button onClick={() => { fileInput.current.click() }}>Upload</Button>
      </label>
    </div>
  )
}
