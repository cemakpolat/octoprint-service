$(document).ready(function () {

    firstPageLoading();

    // left menu panel
    $(".section").on("click", function (e) {
        e.preventDefault();
        if ($(this).hasClass("deactivated")) {
            $(".content").hide();
            $(".section").removeClass("activated").addClass("deactivated");
            $(this).removeClass("deactivated").addClass("activated")
            $("#" + this.id + "-view").show();

            // start the communication with the backend
            initiateDataLoading(this.id);

        } else {
            console.log("same selected, do nothing")
        }
    });

    $("#docker-status-table").on("click", '.deactivate-btn', function (e) {
        e.preventDefault();
        var dockerid = $(this).parent().parent().find('.docker-id').attr('name')
        console.log(dockerid);
        dockerManager.stopDocker(dockerid);
    });

    $("#docker-status-table").on("click", '.activate-btn', function (e) {
        e.preventDefault()
        var dockerid = $(this).parent().parent().find('.docker-id').attr('name')
        console.log(dockerid)
        dockerManager.startDocker(dockerid);

    });
    $("#print-models-btn").on("click", function (e) {
        // send models to the printer
        productManagement.sendPrintRequest();
        $(".printable-asset").removeClass('clicked').addClass("white-border").removeClass('black-border');
    });

    $(document).on('click', '.printable-asset', function (e) {
        e.preventDefault();
        console.log($(this).children(".wrimagecard-topimage_title").attr("title"))
        if ($(this).hasClass("clicked")) {
            $(this).removeClass('clicked')
            $(this).addClass("white-border").removeClass('black-border');
            productManagement.removeSelectedModel($(this).children(".wrimagecard-topimage_title").attr("title"));
        } else {
            $(this).addClass("black-border").removeClass('white-border');
            $(this).addClass("clicked")
            productManagement.addSelectedModel($(this).children(".wrimagecard-topimage_title").attr("title"));
        }
    });

    $("#startDockers").on("click", function (e) {
        var printernumber = $("#dockerCount").val()
        if (printernumber && $.isNumeric(printernumber)) {
            console.log("dockers will be started")
            dockerManager.startAllDockers(printernumber)
        } else {
            console.log("please provide the number")
        }
    });

    $("#stopDockers").on("click", function (e) {
        var printernumber = $("#dockerCount").val()
        if (printernumber && $.isNumeric(printernumber)) {
            console.log("dockers will be stopped")
            dockerManager.stopAllDockers()
        } else {
            console.log("please provide the number")
        }
    });

    $("#stopDataStreaming").on("click", function (e) {
        stopDataLoading();
    });
    $("#startDataStreaming").on("click", function (e) {
        initiateDataLoading("setup-environment"); // 
    });

    $(document).on('click', '.startPrinter', function (e) {
        e.preventDefault();
        var tuple = $(this).closest(".printer-item").attr('printer-name-port');
        var values = tuple.split(",");
        printingManager.startPrintingProcess(values[0], values[1]);

    });

    $(document).on('click', '.stopPrinter', function (e) {
        e.preventDefault();
        var tuple = $(this).closest(".printer-item").attr('printer-name-port');
        var values = tuple.split(",");
        printingManager.stopPrintingProcess(values[0], values[1]);
    });

    $(document).on('click', '.resumePrinter', function (e) {
        e.preventDefault();
        var tuple = $(this).closest(".printer-item").attr('printer-name-port');
        var values = tuple.split(",");
        printingManager.resumePrintingProcess(values[0], values[1]);
    });

    $(document).on('click', '.pausePrinter', function (e) {
        e.preventDefault();
        var tuple = $(this).closest(".printer-item").attr('printer-name-port');
        var values = tuple.split(",");
        printingManager.pausePrintingProcess(values[0], values[1]);
    });


    function firstPageLoading() {
        $(".ss-menu").ssMenu(); // used for left menu
        $(".content").hide(); // hide all data
        $("#setup-environment-view").show(); // show only the load apps
        initiateDataLoading("setup-environment"); // 
    }

    function stopDataLoading() {

        dockerManager.stopDataLoading();
        productManagement.stopDataLoading();
        printingManager.stopDataLoading();
    }

    function initiateDataLoading(sectionId) {
        console.log("The selected item id: " + sectionId)
        stopDataLoading();
        if (sectionId == "setup-environment") {
            dockerManager.starDataLoading();
        } else if (sectionId == "product-models") { 
            productManagement.getPrintableProductModels();
            productManagement.starDataLoading();
        } else if (sectionId == "printing-monitoring") {
            dockerManager.starDataLoading();
            printingManager.startDataLoading();
        } else if (sectionId == "product-monitoring") {
            productMonitoring.starDataLoading();
        } else if (sectionId == "user-profile"){
            
        }
    }
    $('#upload').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;

        if (ins == 0) {
            $('#msg').html('<span style="color:red">Select at least one file</span>');
            return;
        }

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }

    });


});