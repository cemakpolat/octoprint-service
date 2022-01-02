
function buildUrl(url, port, rest){
    return url+":"+port+rest;
}

function removeItemOnce(arr, value) {
    const index = arr.indexOf(value);
    if (index > -1) {
    arr.splice(index, 1);
  }
  return arr;
}

var config = {
    port : 8001,
    url: "http://localhost",
    octoRestPort : 8080    
}

function toDateTime(secs) {
    const t = new Date(1970, 0, 1); // Epoch
    t.setSeconds(secs);
    return t;
}