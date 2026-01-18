// Get temperature and humidity from input
var temp = msg.payload.temperature;
var humidity = msg.payload.humidity;

// Check if data is valid
if (typeof temp !== 'number' || typeof humidity !== 'number') {
    node.warn("Invalid data");
    return null;
}

// Calculate Dew Point
var a = 17.27;
var b = 237.7;
var alpha = ((a * temp) / (b + temp)) + Math.log(humidity / 100.0);
var dewPoint = (b * alpha) / (a - alpha);

// Calculate Absolute Humidity
var e = Math.exp((17.67 * temp) / (temp + 243.5));
var absoluteHumidity = (6.112 * e * humidity) / (461.5 * (temp + 273.15));

// Calculate Depression
var dewPointDepression = temp - dewPoint;

// Get Timestamp
var now = new Date();
var timestamp = now.toLocaleString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
});

var isoTimestamp = now.toISOString();

// ============================================================================
// OUTPUT: SEND OBJECT TO DASHBOARD UI ONLY
// ============================================================================
// No Telegram formatting - just raw data for dashboard gauges

msg.payload = {
    temperature: parseFloat(temp.toFixed(2)),
    humidity: parseFloat(humidity.toFixed(2)),
    dewPoint: parseFloat(dewPoint.toFixed(2)),
    absoluteHumidity: parseFloat(absoluteHumidity.toFixed(2)),
    dewPointDepression: parseFloat(dewPointDepression.toFixed(2)),
    timestamp: timestamp,
    isoTimestamp: isoTimestamp,
    location: "Berlin, Germany"
};

// Send to dashboard
return msg;
