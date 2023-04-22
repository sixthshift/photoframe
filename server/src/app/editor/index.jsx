import React, { useContext } from 'react'

import ImageEditor, { } from 'react-filerobot-image-editor'
import { Modal } from 'react-bootstrap'

import { PhotoContext } from '../photoProvider'

import config from './config'

const EditorModal = ({ title = '', children }) => {
  const [photo, setPhoto] = useContext(PhotoContext).photo
  const onClose = () => {
    setPhoto(null)
  }
  return (
    <Modal fullscreen show={!!photo} onHide={onClose}>
      <Modal.Header closeButton>{title}</Modal.Header>
      <Modal.Body>{{ ...children }}</Modal.Body>
    </Modal>
  )
}

export default function Editor () {
  const { gallery: [, setGallery], photo: [photo, setPhoto] } = useContext(PhotoContext)

  const uploadPhoto = async (photo) => {
    const formData = new FormData()
    formData.append('photo', photo)

    return fetch('upload', { method: 'POST', body: formData })
      .then(response => response.json())
  }

  const deletePhoto = async (filename) => {
    return fetch('delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ filename })
    })
      .then(response => response.json())
  }

  return photo
    ? <EditorModal>
      <ImageEditor
        {...config({
          photo,
          onClose: () => {
            setPhoto(null)
          },
          onSave: (imageData) => {
            return fetch(imageData.imageBase64)
              .then(response => response.blob())
              .then(blob => { return new File([blob], decodeURIComponent(imageData.fullName), { type: blob.type }) })
              .then(uploadPhoto)
              .then((metadata) => {
                setGallery(metadata)
                return metadata.find((photoMetadata) => photoMetadata.name === decodeURIComponent(imageData.fullName))
              })
              .catch((err) => { console.error(err) })
          },
          onDisplay: (photo) => {
            return fetch('display', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(photo)
            })
          },
          onDelete: (imageData) => {
            return deletePhoto(imageData.fullName)
              .then(setGallery)
          }
        })
        }
      />
    </EditorModal>
    : null
}
