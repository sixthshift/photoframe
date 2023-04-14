const fs = require('fs')
const path = require('path')
const sharp = require('sharp')

module.exports = class Gallery {
  constructor (directory) {
    this.directory = directory
  }

  async metadata () {
    return await Promise.all(
      fs.readdirSync(this.directory)
        .map(async (filename) => {
          const absolutePath = path.join(this.directory, filename)
          try {
            const photo = await sharp(absolutePath).metadata()
            return {
              src: path.join('photo', filename),
              path: absolutePath,
              width: photo.width,
              height: photo.height
            }
          } catch (error) {
            console.error(absolutePath + ' ' + error)
          }
        })
    )
  }

  async randomPhoto () {
    const metadata = await this.metadata()
    return metadata[Math.floor(Math.random() * metadata.length)].path
  }

  write (filename, data) {
    const absolutePath = path.join(this.directory, filename)
    fs.writeFileSync(absolutePath, data)
  }
}
