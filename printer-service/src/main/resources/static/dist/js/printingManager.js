const printingManager = {
    printerStatuses: [],
    dataLoadingFromPrinters: null,
    port: config.port,
    restport: config.octoRestPort,
    url: config.url,

    stopDataLoading: function () {
        clearInterval(this.dataLoadingFromPrinters);
    },

    startDataLoading: function () {
        this.getAllPrinterStatuses();
        this.dataLoadingFromPrinters = setInterval(this.getAllPrinterStatuses, 10000);
    },

    getStatusFromService: function (printerName, dockerPort, restUrl, callback) {
        console.log(dockerPort, restUrl);
        $.ajax({
            type: "GET",
            url: buildUrl(printingManager.url, printingManager.restport, restUrl),
            dataType: "json",
            data: {
                'port': dockerPort
            },
        }).done(function (jsondata) {
            let data = jsondata['status']
            data = JSON.parse(data);
            console.log(data);
            callback( printingManager.formPrinterStatusData(data));

        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.log("Error occured with this data", jqXHR, textStatus, errorThrown)
        });
    },

    getAllPrinterStatuses: function () {
        this.printerStatuses = []; // clean the printer list
        // let dockers = infrastructureManager.activeDockerContainers
        for (let i = 0; i < infrastructureManager.activeDockerContainers.length; i++) {
            printingManager.updatePrinterStatus(infrastructureManager.activeDockerContainers[i].name, infrastructureManager.activeDockerContainers[i].port);

        }
    },

    updatePrinterStatus: function (printerName, printerPort) {
        this.getStatusFromService(printerName, printerPort, "/product/status", function (data) {
            printingManager.updatePrinterItem({
                name: printerName,
                port: printerPort
            }, data)
        });
    },

    updatePrinterItem: function (docker, data) {
        this.printerStatuses.push({
            docker: docker,
            data: data
        });
        componentGenerator.addPrinter(docker.name, docker.port, data);
    },

    formPrinterStatusData: function (data) {
        let updated_data = {
            bedTemperature: '0',
            extruderTemperature: '0',
            estimatedFilamentUsage: '0',
            estimatedPrintTime: '0',
            progress: '0',
            status: 'OPERATIONAL'
        };
        if ('bedTemperature' in data)
            updated_data['bedTemperature'] = data['bedTemperature'];
        if ('estimatedFilamentUsage' in data)
            updated_data['bedTemperature'] = data['bedTemperature'];
        if ('estimatedPrintTime' in data)
            updated_data['estimatedPrintTime'] = data['estimatedPrintTime'];
        if ('extruderTemperature' in data)
            updated_data['extruderTemperature'] = data['extruderTemperature'];
        if ('progress' in data)
            updated_data['progress'] = Math.round(data["progress"] * 100) / 100;
        if ('status' in data)
            updated_data['status'] = data['status'];
        return updated_data;
    },
    startPrintingProcess: function (printerName, printerPort) {
        this.getStatusFromService(printerName, printerPort, "/printer/status", function (data) {
            componentGenerator.updatePrinter(printerName, printerPort, data);
        });

    },

    stopPrintingProcess: function (printerName, printerPort) {
        this.getStatusFromService(printerName, printerPort, "/printer/stop", function (data) {
            const updatedData = printingManager.formPrinterStatusData(data);
            componentGenerator.updatePrinter(printerName, printerPort, updatedData);
        });

    },

    pausePrintingProcess: function (printerName, printerPort) {
        this.getStatusFromService(printerName, printerPort, "/printer/pause", function (data) {
            const updatedData = printingManager.formPrinterStatusData(data);
            componentGenerator.updatePrinter(printerName, printerPort, updatedData);

        });

    },

    resumePrintingProcess: function (printerName, printerPort) {
        this.getStatusFromService(printerName, printerPort, "/printer/resume", function (data) {
            componentGenerator.updatePrinter(printerName, printerPort, data);
        });

    }
};