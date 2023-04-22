module.exports = class URL {
  constructor ({ baseUrl = '', path = '', options = {} }) {
    this.baseUrl = baseUrl
    this.path = Array.isArray(path) ? path : [path]
    this.options = options
  }

  toURL () {
    let url = ''
    url += this.baseUrl
    url += !!this.baseUrl && !!this.path ? '/' : ''
    url += this.path.map(this._encode).join('/')
    url += Object.keys(this.options).length !== 0 ? '?' + Object.entries(this.options).map(([key, value]) => (this._encode(key) + '=' + this._encode(value))).join('&') : ''
    return url
  }

  _encode (string) {
    if (decodeURIComponent(string) === string) {
      return encodeURIComponent(string)
    } else {
      return string
    }
  }
}
