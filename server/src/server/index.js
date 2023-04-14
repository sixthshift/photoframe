require('dotenv').config()

const { program } = require('commander')

const Gallery = require('./model/gallery')
const serve = require('./serve')

program
  .argument('<string>', 'photo directory')
  .action(async (photoDirectory) => {
    const gallery = new Gallery(photoDirectory)
    serve(gallery)
  })
  .parse()
