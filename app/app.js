const express = require('express');
const path = require('path');
const Logger = require('js-logger');

// Server stuff
const app = express();
const port = process.env.PORT || 80;
app.set('view engine', 'ejs');

// Logger stuff
Logger.useDefaults();
const logger = Logger.get("app");

// Endpoints
app.use(express.static('public'));

app.get('/', function(req, res) {
    res.render("index");
});

logger.info(`Listening on http://localhost:${port}`);
const server = app.listen(port);