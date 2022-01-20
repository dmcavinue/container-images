const http = require('http')
const url = require('url')
const puppeteer = require('puppeteer');
const mqtt = require('mqtt');
const util = require('util');

// MQTT Options
const mqttClientId = `ubiquiti_watcher_${Math.random().toString(16).slice(3)}`;
var mqttHost = '';
if(process.env.MQTT_HOST) {
    mqttHost = process.env.MQTT_HOST;
}
var mqttPort = '1883';
if(process.env.MQTT_PORT) {
    mqttPort = process.env.MQTT_PORT;
}
var mqttUsername = 'mqtt';
if(process.env.MQTT_USERNAME) {
    mqttUsername = process.env.MQTT_USERNAME;
}
var mqttPassword = 'password';
if(process.env.MQTT_PASSWORD) {
    mqttPassword = process.env.MQTT_PASSWORD;
}
var mqttTopic = 'ubiquiti-watcher';
if(process.env.MQTT_TOPIC) {
    mqttTopic = process.env.MQTT_TOPIC;
}
const mqttConnectUrl = `mqtt://${mqttHost}:${mqttPort}`

// Ubiquiti Options
var refreshUrl = 'https://store.ui.com/';
if(process.env.REFRESH_URL) {
    refreshUrl = process.env.REFRESH_URL;
}
var refreshRate = 10000;
if(process.env.REFRESH_RATE) {
    refreshRate = Number(process.env.REFRESH_RATE)*1000;
}
var showAllAvailableFilters = [""];
if(process.env.PRODUCT_FILTERS) {
    showAllAvailableFilters = process.env.PRODUCT_FILTERS.split(",");
}
var desiredProducts = [""];
if(process.env.DESIRED_PRODUCTS) {
    desiredProducts = process.env.DESIRED_PRODUCTS.split(",");
}

// MQTT Client
const mqttClient = mqtt.connect(mqttConnectUrl, {
  mqttClientId,
  clean: true,
  connectTimeout: 4000,
  username: mqttUsername,
  password: mqttPassword,
  reconnectPeriod: 1000,
});

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: '/usr/bin/chromium-browser',
        args: [
        "--no-sandbox",
        "--disable-gpu",
        ]
    });
    const page = await browser.newPage();
    var getAvailable = async function(){
        await page.goto(refreshUrl, {
            timeout: 0,
            waitUntil: 'networkidle2',
        });        

        var success = function(product){
          console.log(util.format('%s/products/%s : %s', mqttTopic, product.toLowerCase(), Date.now().toString()));
          mqttClient.publish(util.format('%s/products/%s', mqttTopic, product.toLowerCase()), Date.now().toString(), { qos: 0, retain: false }, (error) => {
            if (error) {
              console.error(error)
            }
          })
        }
        var functionToInject = function(){
            return document.querySelector("#app").__vue__.appData.cartAccessories.map(a=>a.title);
        }
        var toWait = Math.floor((refreshRate+Math.random()*refreshRate)/1000);
        var data = await page.evaluate(functionToInject);
        var foundItems = data.filter(a=>desiredProducts.some(b=>b==a));
        if(foundItems.length){
          foundItems.forEach(element => {
            success(element);
          });            
        }
        console.log((foundItems.length?"":"Desired product(s) not found. ") + 
            "Waiting " +  toWait + "s to check again. ");
        // if(showAllAvailableFilters.length){
        //   console.log("Available Products: ");
        //   console.log(data.filter(a=>showAllAvailableFilters.some(b=>a.startsWith(b))));
        // }
        mqttClient.publish(util.format('%s/timestamp', mqttTopic), Date.now().toString(), { qos: 0, retain: false }, (error) => {
          if (error) {
            console.error(error)
          }
        })
        setTimeout(getAvailable, toWait*1000);
    }
    getAvailable();
})();
