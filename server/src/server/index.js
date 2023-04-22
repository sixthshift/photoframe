require('dotenv').config()

const { program } = require('commander')
const path = require('path')

const Frame = require('./model/frame')
const Gallery = require('./model/gallery')
const serve = require('./serve')

program
  .argument('<string>', 'photo directory')
  .action(async (photoDirectory) => {
    serve(
      new Gallery(photoDirectory),
      new Frame(path.resolve('../client/src/run.py'))
    )
  })
  .parse()
