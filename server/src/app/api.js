export default {
  async delete (filename) {
    return fetch('delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename })
    })
      .then(response => response.json())
  },
  async display (photo) {
    return fetch('display', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(photo)
    })
  },
  async metadata () {
    return fetch('metadata')
      .then((response) => response.json())
  },
  async upload (photo) {
    const formData = new FormData()
    formData.append('photo', photo)

    return fetch('upload', { method: 'POST', body: formData })
      .then(response => response.json())
  }
}
