const path = require('path')
const express = require('express')

const uploadMiddleware = require('./middleware/uploadMiddleware')

const port = process.env.PORT || 3000

module.exports = (gallery) => {
  const app = express()

  app.use(express.json())

  app.use(express.static(path.resolve('public')))

  app.use('/photo', express.static(gallery.directory))

  app.get('/photo', async (_, res) => {
    app.locals.photo ??= await gallery.randomPhoto()
    res.sendFile(app.locals.photo.path)
  })

  app.post('/display', (req, res) => {
    app.locals.photo = req.body
    res.json(req.body)
  })

  app.get('/metadata', async (_, res) => {
    res.json(await gallery.metadata())
  })

  app.post('/upload', uploadMiddleware, async (req, res) => {
    gallery.write(req.file.filename, req.file.data)
    res.redirect('/metadata')
  })

  app.listen(port, () => {
    console.info(`Photo frame server started on port ${port}`)
  })
}
