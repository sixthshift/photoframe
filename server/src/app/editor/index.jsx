import React, { useContext } from 'react'

import ImageEditor, { } from 'react-filerobot-image-editor'
import { Modal } from 'react-bootstrap'

import { PhotoContext } from '../photoProvider'

import Config from './config'
import api from '../api'

function dataUrlToBlob (dataUrl) {
  return fetch(dataUrl)
    .then(response => response.blob())
}

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
  if (photo) {
    const config = Config({
      photo,
      onClose: () => {
        setPhoto(null)
      },
      onSave: (imageData) => {
        const newPath = photo.path.name.endsWith('_edited') ? (photo.path.name + photo.path.ext) : photo.path.name + '_edited' + '.png'
        return dataUrlToBlob(imageData.imageBase64)
          .then(blob => { return new File([blob], newPath, { type: blob.type }) })
          .then(api.upload)
          .then((metadata) => {
            setGallery(metadata)
            return metadata.find((photoMetadata) => photoMetadata.name === newPath)
          })
          .catch((err) => { console.error(err) })
      },
      onDisplay: api.display,
      onDelete: (imageData) => {
        return api.delete(imageData.fullName)
          .then(setGallery)
      }
    })

    return (
      <EditorModal>
        <ImageEditor {...config} />
      </EditorModal>
    )
  } else {
    return null
  }
}
