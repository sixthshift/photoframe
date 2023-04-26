const cron = require('node-cron')
const path = require('path')
const express = require('express')

const uploadMiddleware = require('./middleware/uploadMiddleware')

const port = process.env.PORT || 80

module.exports = (gallery, frame) => {
  const app = express()
  app.use(express.json())

  app.use(express.static(path.resolve('public')))
  app.use('/photo', express.static(gallery.directory))

  app.get('/photo', async (_, res) => {
    if (app.locals.photo) {
      res.sendFile(path.format(app.locals.photo.path))
    } else {
      res.sendStatus(503)
    }
  })

  app.post('/display', (req, res) => {
    app.locals.photo = req.body
    const url = req.headers.origin + '/' + req.body.src
    frame.display({ url, orientation: 'landscape' })
    res.sendStatus(200)
  })

  app.get('/metadata', async (_, res) => {
    res.json(await gallery.metadata())
  })

  app.post('/upload', uploadMiddleware, async (req, res) => {
    gallery.write(decodeURIComponent(req.file.filename), req.file.data)
    res.json(await gallery.metadata())
  })

  app.post('/delete', async (req, res) => {
    gallery.delete(req.body.filename)
    res.json(await gallery.metadata())
  })

  app.listen(port, () => {
    console.info(`Photoframe server started on port ${port}`)
  })

  gallery.randomPhoto()
    .then((photo) => {
      app.locals.photo = photo
    })

  cron.schedule('0 0 0 * * *', async () => {
    app.locals.photo = await gallery.randomPhoto()
    const url = 'http://localhost:' + port + '/' + app.locals.photo.src
    const timeStamp = new Date().toLocaleString('en-AU', { timeZone: 'Australia/Sydney' })
    console.info(`Scheduled refresh | ${timeStamp}`)
    frame.display({ url, orientation: 'landscape' })
  }).start()
}
