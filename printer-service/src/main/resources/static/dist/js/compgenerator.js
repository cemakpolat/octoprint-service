var componentGenerator = {

    addDockerDetails: function (index, item) {
        var div = '<tr>' +
            '<th scope="row">' + index + '</th>' +
            '<td class="docker-id" name=' + item.name + '>' + item.name + '</td>' +
            '<td class="docker-port">' + item.port + '</td>' +
            '<td class="docker-status">' + item.status + '</td>' +
            '<td><button class="deactivate-btn btn-danger">Stop</button></td>' +
//            '<td><button class="activate-btn btn-success">Activate</button></td>' +
            '</tr>';
        $("#docker-status-table").children("tbody").append(div);
    },

    cleanDockerDetails: function () {

        $("#docker-status-table").children("tbody").empty();
    },
    cleanPrintableAssets: function () {
        $('#assetslist').empty();
    },
    cleanMonitoredProducts: function () {
        $("#product-status-table").children("tbody").empty();
    },
    
    addNewPrintableAsset: function (index, item) {
        var div = '<div class="col-md-3 col-sm-4">' +
            '<div class="wrimagecard wrimagecard-topimage white-border printable-asset">' +
            '<div class="wrimagecard-topimage_header" style="background-color: grau">' +
            '<center><img width="100%" height="300px" src="dist/img/img' + index + '.jpeg" /></center>' +
            '</div>' +
            '<div class="wrimagecard-topimage_title" title="' + item + '">' +
            '<h5>' + item +
            '<div class="pull-right badge" id="WrControls">1</div></h5>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>';

        $('#product-models-view').children(":first").append(div);
    },
    getRandom:function(max, min){
          return Math.floor(Math.random() * (max - min + 1) + min)
    },
    
    addAssetNameToPrintableList: function (number) {
        this.cleanMonitoredProducts();
        for (var i = 1; i < number; i++) {

             var div = '<tr>' +
            '<th scope="row">' + i + '</th>' +
            '<td class="product-id" name=' + + '>' + "Product" + '</td>' +
            '<td class="product-status">' + "Waiting"+ '</td>' +
            '<td class="printing-percentage">'+this.getRandom(100,0)+'%</td>' +
            '<td class="delivery-status"><div style="width:100%"></td>' +
            '</tr>';

            $("#product-status-table").children("tbody").append(div);

        }
    },
    

    addPrinter: function(printerName, printerPort, printerData){
        $('.printer-item[printer-name-port="'+printerName+","+printerPort+'"]').remove();        

        var div = '<div class="printer-item col-md-3 col-sm-4" printer-name-port="'+printerName+','+printerPort+'">'+
           '<div class="wrimagecard wrimagecard-topimage white-border td-printer">'+
              '<div class="wrimagecard-topimage_header" style="background-color: rgba(22, 160, 133, 0.1);margin:5px;">'+
                 '<center><img width="50%" style="border-radius:50%" height="100" src="dist/img/printer1.png" /></center>'+
              '</div>'+
              '<h4  style="margin:5px">'+printerName+'</h4>'+
              '<div>'+
                 '<table style="margin:5px">'+
                    '<tr>'+
                       '<td>bedTemperature: </td>'+
                       '<td>'+ printerData.bedTemperature +'</td>'+
                    '</tr>'+
                    '<tr>'+
                       '<td>estimatedFilamentUsage: </td>'+
                       '<td>'+ printerData.estimatedFilamentUsage +'</td>'+
                    '</tr>'+
                    '<tr>'+
                       '<td>estimatedPrintTime: </td>'+
                       '<td>'+ printerData.estimatedPrintTime +'</td>'+
                    '</tr>'+
                    '<tr>'+
                       '<td>extruderTemperature: </td>'+
                       '<td>'+ printerData.extruderTemperature +'</td>'+
                    '</tr>'+
                    '<tr>'+
                       '<td>progress: </td>'+
                       '<td>'+ printerData.progress +'</td>'+
                    '</tr>'+
                    '<tr>'+
                       '<td>status: </td>'+
                       '<td>'+ printerData.status +'</td>'+
                    '</tr>'+
                 '</table>'+
              '</div>'+
              '<div style="margin-top:10px; position: relative;">'+
                 '<button type="button" class="startPrinter btn-sm btn-success">Start</button>'+
                 '<button style="margin:1px" type="button" class="stopPrinter btn-sm btn-primary">Stop</button>'+
                 '<button style="margin:1px" type="button" class="resumePrinter btn-sm btn-warning">Resume</button>'+
                 '<button  type="button" class="pausePrinter btn-sm btn-dark">Pause</button>'+
              '</div>'+
           '</div>'+
        '</div>'+
        '</div>';
        $('#allprinters').append(div);
    },
    updatePrinter: function(printerName, printerPort, printerData){
        this.addPrinter(printerName, printerPort, printerData);
    },
    
    addPrintingAssetsStatuses: function(printingAssets){
          this.cleanMonitoredProducts();
        for (var i = 0; i < printingAssets.length; i++) {

             var div = '<tr>' +
            '<th scope="row">' + (i+1) + '</th>' +
            '<td class="product-id">' + printingAssets[i].name + '</td>' +
            '<td class="product-status">' + printingAssets[i].status+ '</td>' +
            '<td class="product-starting-time">' + printingAssets[i].started+ '</td>' +
            '<td class="printing-percentage">'+printingAssets[i].percentage+'%</td>' +
            '<td class="assigned-printer">'+printingAssets[i].assignedPrinterName+'</td>' +
            '</tr>';

            $("#product-status-table").children("tbody").append(div);

        }
    }

};