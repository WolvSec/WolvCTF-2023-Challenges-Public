const express = require('express')
const app = express()
const port = 80

app.get('/', (req, res) => {
    res.sendFile('public_info.json', { root: __dirname })
})

app.get('/logs', (req, res) => {
    res.sendFile('logs.txt', { root: __dirname })
})


app.listen(port, () => {
    console.log('Listening on port', port)
})