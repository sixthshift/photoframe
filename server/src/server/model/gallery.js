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

  async metadatum (filePath) {
    const metadata = await sharp(filePath).metadata()
    const hash = crypto.createHash('md5').update(JSON.stringify(metadata)).digest('hex')
    const parsed = path.parse(filePath)

    return {
      name: parsed.base,
      src: new URL({ path: ['photo', parsed.base], options: { hash } }).toURL(),
      path: parsed,
      width: metadata.width,
      height: metadata.height
    }
  }

  async metadata () {
    return (
      await Promise.all(
        fs.readdirSync(this.directory)
          .filter(filename => !path.parse(filename).name.endsWith('_edited'))
          .map(async (filename) => {
            const absolutePath = path.join(this.directory, filename)
            try {
              const metadatum = await this.metadatum(absolutePath)
              try {
                const editedPath = { ...metadatum.path }
                editedPath.name += '_edited'
                editedPath.base = editedPath.name + '.png'
                const editedMetaDatum = await this.metadatum(path.format(editedPath))
                editedMetaDatum.original = metadatum
                return editedMetaDatum
              } catch (error) {
                // Errors here are fine, as we do not expect all images to have edits
                return metadatum
              }
            } catch (error) {
              console.debug(absolutePath + ' ' + error)
              return undefined
            }
          })
      )
    )
      .filter(data => !!data)
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
