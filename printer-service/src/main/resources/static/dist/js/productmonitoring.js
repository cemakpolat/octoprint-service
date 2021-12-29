var productMonitoring = {
    assetsInPrintingQueue: [],
    port: config.port,
    url: config.url,
    dataLoading: null,
    uploadTime: 5000,
    
    stopDataLoading: function () {
        clearInterval(this.dataLoading)
    },
    starDataLoading: function () {
        this.dataLoading = setInterval(this.getCurrentStatusOfProducts, this.uploadTime);
    },
    
    getCurrentStatusOfProducts: function () {
        productMonitoring.assetsInPrintingQueue = []
        $.get(buildUrl(productMonitoring.url, productMonitoring.port, "/printers/assets/status"))
            .done(function (jsonData) {
                for (item in jsonData){
                    productMonitoring.assetsInPrintingQueue.push(jsonData[item]);
                }
                productMonitoring.getPrintingAssetsPercentage();
            }).fail(function (jsondata) {
                console.log("Error occured with this data", jsondata)
            });
    },

    getPrintingAssetsPercentage: function(){
              
        for (item in productMonitoring.assetsInPrintingQueue){
            if (productMonitoring.assetsInPrintingQueue[item].status == "printing"){
                
                for (var i = 0; i < dockerManager.activeDockerContainers.length; i++) {
                    if(productMonitoring.assetsInPrintingQueue[item].assignedPrinterName == dockerManager.activeDockerContainers[i].name){
                        this.updatePercentage(productMonitoring.assetsInPrintingQueue[item], dockerManager.activeDockerContainers[i].port);
                        break;
                    }
                }
            }else{
                productMonitoring.assetsInPrintingQueue[item].percentage = 0;
                productMonitoring.assetsInPrintingQueue[item].started = "-";
                productMonitoring.assetsInPrintingQueue[item].assignedPrinterName = "-";
            }      
        }
        
    },
    updatePercentage: function (item,dockerPort){
      $.ajax({
            type: "GET",
            url: buildUrl(printingManager.url, printingManager.restport, "/product/status"),
            dataType: "json",
            data: {
                'port': dockerPort
            },
        }).done(function (jsondata) {
          
            data = jsondata['content']
            data = JSON.parse(data)
            console.log(data);
            for (elem in productMonitoring.assetsInPrintingQueue){
                if (productMonitoring.assetsInPrintingQueue[elem].name === item.name){
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
    },
    uploadFiles: function(form_data){
        $.ajax({
            url: buildUrl(config.url, config.port, "/printers/assets/upload"), 
            dataType: 'json', 
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) {
                $('#msg').html('');
                $.each(response, function (key, data) {							
                    if(key !== 'message') {
                        $('#msg').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
    }
    
}