module.exports = {
  build: {
    outDir: 'public',
    sourcemap: process.env.NODE_ENV === 'development' ? 'inline' : false
  }
}
