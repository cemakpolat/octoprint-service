
function getPrinterStatus() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: 'http://localhost:8080/printerStatus',
            type: 'GET',
            data: {
                key: 'value',
            },
            success: function (data) {
                resolve(data)
            },
            error: function (error) {
                reject(error)
            },
        })
    })
}