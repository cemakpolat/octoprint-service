var productManagement = {
    selectedModelsNames: [],
    dataLoadingFromPrinters: null,
    printableModels: null,
    port: config.port,
    url: config.url,

    stopDataLoading: function () {
        clearInterval(this.dataLoadingFromPrinters);
    },

    starDataLoading: function () {
        this.dataLoadingFromPrinters = setInterval(this.getPrintableProductModels, 30000);
        console.log(this.dataLoadingFromPrinters);
    },

    addSelectedModel: function (model) {
        productManagement.selectedModelsNames.push(model);
    },

    removeSelectedModel: function (model) {
        removeItemOnce(productManagement.selectedModelsNames, model);
    },
    
    cleanSelectedModelList: function(){
      this.selectedModelsNames = [];  
    },
    
    getPrintableProductModels: function () {
        componentGenerator.cleanPrintableAssets();
        this.printableModels = []
        $.get(buildUrl(productManagement.url, productManagement.port, "/models"))
            .done(function (data) {
                result = JSON.parse(data);
                printableModels = result["result"];
                for (var i = 0; i < printableModels.length; i++) {
                    componentGenerator.addNewPrintableAsset(i + 1, printableModels[i]);
                }
                this.printableModels = printableModels;
            }).fail(function () {
                console.error("Files cannot be received from the folder");
            });
    },
    
    sendPrintRequest: function () {
        console.log("list to be sent", productManagement.selectedModelsNames);
        $.post(buildUrl(productManagement.url, productManagement.port, "/printers/select"), {
                products: productManagement.selectedModelsNames
            },
            function (returnedData) {
                data = JSON.parse(returnedData);
                console.log("print request", data);
                productManagement.cleanSelectedModelList();
            }).fail(function (data) {
                console.log("error", data);
            });
    }

}