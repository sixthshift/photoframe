const crypto = require('crypto')
const fs = require('fs')
const path = require('path')
const sharp = require('sharp')

const URL = require('./url')

module.exports = class Gallery {
  constructor (directory) {
    this.directory = directory
    if (!fs.existsSync(this.directory)) {
      console.info(`Creating directory at ${this.directory}`)
      fs.mkdirSync(this.directory, { recursive: true })
    }
    if (!fs.lstatSync(this.directory).isDirectory()) {
      throw new Error(`${this.directory} is not a directory`)
    }
    console.info('Photoframe directory: ' + this.directory)
  }

  async metadata () {
    return (await Promise.all(
      fs.readdirSync(this.directory)
        .map(async (filename) => {
          const absolutePath = path.join(this.directory, filename)
          try {
            const metadata = await sharp(absolutePath).metadata()
            const hash = crypto.createHash('md5').update(JSON.stringify(metadata)).digest('hex')

            return {
              name: filename,
              src: new URL({ path: ['photo', filename], options: { hash } }).toURL(),
              path: absolutePath,
              width: metadata.width,
              height: metadata.height
            }
          } catch (error) {
            console.debug(absolutePath + ' ' + error)
            return undefined
          }
        })
    )).filter(data => !!data)
  }

  async randomPhoto () {
    const metadata = await this.metadata()
    return metadata[Math.floor(Math.random() * metadata.length)]
  }

  write (filename, data) {
    const absolutePath = path.join(this.directory, filename)
    fs.writeFileSync(absolutePath, data)
  }

  delete (filename) {
    const absolutePath = path.join(this.directory, filename)
    fs.unlinkSync(absolutePath)
  }
}
