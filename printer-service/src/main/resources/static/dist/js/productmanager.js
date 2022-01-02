const productManagement = {
    selectedModelsNames: [],
    dataLoadingFromPrinters: null,
    printableModels: null,
    port: config.port,
    url: config.url,

    stopDataLoading: function () {
        clearInterval(this.dataLoadingFromPrinters);
    },

    starDataLoading: function () {
        this.getPrintableProductModels();
        this.dataLoadingFromPrinters = setInterval(this.getPrintableProductModels, 30000);
        console.log(this.dataLoadingFromPrinters);
    },

    addSelectedModel: function (model) {
        productManagement.selectedModelsNames.push(model);
    },

    removeSelectedModel: function (model) {
        removeItemOnce(productManagement.selectedModelsNames, model);
    },

    cleanSelectedModelList: function () {
        this.selectedModelsNames = [];
    },

    getPrintableProductModels: function () {
        componentGenerator.cleanPrintableAssets();
        this.printableModels = []
        $.get(buildUrl(productManagement.url, productManagement.port, "/models"))
            .done(function (data) {
                // console.log(data);
                const models = data["message"];
                for (let i = 0; i < models.length; i++) {
                    componentGenerator.addNewPrintableAsset(i + 1, models[i]);
                }
                this.printableModels = models;
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
                // console.log("print request", returnedData["message"]);
                productManagement.cleanSelectedModelList();
            }).fail(function (data) {
            console.log("error", data);
        });
    },
    uploadFiles: function (form_data) {
        $.ajax({
            url: buildUrl(config.url, config.port, "/printers/assets/upload"),
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post'
        }).done(function (response) {
                $('#msg').html('');
                $.each(response, function (key, data) {
                    if (key !== 'message') {
                        $('#msg').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg').append(data + '<br/>');
                    }
                })

        }).fail(function (jqXHR, textStatus, errorThrown) {
                $('#msg').html(jqXHR.responseText); // display error response
        });
    }

};