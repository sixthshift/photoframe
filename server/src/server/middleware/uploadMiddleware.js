const busboy = require('busboy')

module.exports = (req, _, next) => {
  req.pipe(
    busboy({ headers: req.headers })
      .on('file', (_, file, filename) => {
        const chunks = []
        file.on('data', (data) => {
          chunks.push(data)
        })
        file.on('end', () => {
          req.file = {
            data: Buffer.concat(chunks),
            ...filename
          }
          next()
        })
      })
      .on('error', (err) => {
        next(err)
      })
  )
}
