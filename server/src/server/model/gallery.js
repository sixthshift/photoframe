const crypto = require('crypto')
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
            const metadata = await sharp(absolutePath).metadata()
            const hash = crypto.createHash('md5').update(JSON.stringify(metadata)).digest('hex')
            return {
              name: filename,
              src: path.join('photo', filename) + '?' + hash,
              path: absolutePath,
              width: metadata.width,
              height: metadata.height
            }
          } catch (error) {
            console.error(absolutePath + ' ' + error)
          }
        })
    )
  }

  async randomPhoto () {
    const metadata = await this.metadata()
    return metadata[Math.floor(Math.random() * metadata.length)]
  }

  write (filename, data) {
    const absolutePath = path.join(this.directory, filename)
    fs.writeFileSync(absolutePath, data)
  }
}
