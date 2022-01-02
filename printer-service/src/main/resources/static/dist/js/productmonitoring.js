const productMonitoring = {
    assetsInPrintingQueue: [],
    port: config.port,
    url: config.url,
    dataLoading: null,
    uploadTime: 5000,

    stopDataLoading: function () {
        clearInterval(this.dataLoading)
    },
    starDataLoading: function () {
        this.getCurrentStatusOfProducts();
        this.dataLoading = setInterval(this.getCurrentStatusOfProducts, this.uploadTime);
    },

    getCurrentStatusOfProducts: function () {
        productMonitoring.assetsInPrintingQueue = []
        $.get(buildUrl(productMonitoring.url, productMonitoring.port, "/printers/assets/status"))
            .done(function (jsonData) {
                const data = jsonData["message"];
                for (let item in data) {
                    productMonitoring.assetsInPrintingQueue.push(data[item]);
                }
                productMonitoring.getPrintingAssetsPercentage();
            }).fail(function (jsondata) {
            console.log("Error occured with this data", jsondata)
        });
    },

    getPrintingAssetsPercentage: function () {

        for (let item in productMonitoring.assetsInPrintingQueue) {
            if (productMonitoring.assetsInPrintingQueue[item].status == "printing") {

                for (let i = 0; i < dockerManager.activeDockerContainers.length; i++) {
                    if (productMonitoring.assetsInPrintingQueue[item].assignedPrinterName == dockerManager.activeDockerContainers[i].name) {
                        this.updatePercentage(productMonitoring.assetsInPrintingQueue[item], dockerManager.activeDockerContainers[i].port);
                        break;
                    }
                }
            } else {
                productMonitoring.assetsInPrintingQueue[item].percentage = 0;
                productMonitoring.assetsInPrintingQueue[item].started = "-";
                productMonitoring.assetsInPrintingQueue[item].assignedPrinterName = "-";
            }
        }

    },
    updatePercentage: function (item, dockerPort) {
        $.ajax({
            type: "GET",
            url: buildUrl(printingManager.url, printingManager.restport, "/product/status"),
            dataType: "json",
            data: {
                'port': dockerPort
            },
        }).done(function (jsondata) {
            // console.log(jsondata);
            let data = jsondata['status']
            data = JSON.parse(data)
            // console.log(data);
            for (let elem in productMonitoring.assetsInPrintingQueue) {
                if (productMonitoring.assetsInPrintingQueue[elem].name === item.name) {
                    productMonitoring.assetsInPrintingQueue[elem].percentage = Math.round(data["progress"] * 100) / 100;
                    productMonitoring.assetsInPrintingQueue[elem].started = toDateTime(item.started);
                    break;
                }
            }
            // TODO: Ideal solution is to update all in once, which requires promise usage.
            componentGenerator.cleanMonitoredProducts();
            componentGenerator.addPrintingAssetsStatuses(productMonitoring.assetsInPrintingQueue);
        })
            .fail(function (jqXHR, textStatus, errorThrown) {
                console.log("Error occured with this data", jqXHR, textStatus, errorThrown)
            });
    }

};