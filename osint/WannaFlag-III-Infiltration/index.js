const path = require('path')
const express = require('express')
const app = express()
app.use(express.static(path.join(__dirname, 'website')))

const port = 80

app.listen(port, () => {
    console.log(`App listening on port ${port}`)
})