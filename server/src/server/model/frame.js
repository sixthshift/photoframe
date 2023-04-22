const { exec } = require('child_process')

module.exports = class Frame {
  constructor (entry) {
    this.entry = entry
    console.info('Photoframe device entrypoint: ' + this.entry)
  }

  display ({ url, orientation }) {
    console.info('displaying ' + url)
    const command = `python ${this.entry} --image ${url} --orientation ${orientation}`
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`)
        return
      }
      stdout && console.log(`stdout: ${stdout}`)
      stderr && console.error(`stderr: ${stderr}`)
    })
  }
}
