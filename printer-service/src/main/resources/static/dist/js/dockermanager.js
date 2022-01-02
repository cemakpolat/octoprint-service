const dockerManager = {
    dataLoading: null,
    activeDockerContainers: [],
    port: config.port,
    url: config.url,

    stopDataLoading: function () {
        console.log("stopping the data loading")
        clearInterval(this.dataLoading);
    },

    starDataLoading: function () {
        this.getAllDockers();
        this.dataLoading = setInterval(this.getAllDockers, 10000);
    },

    createDockerList: function (docks) {
        componentGenerator.cleanDockerDetails();
        dockerManager.activeDockerContainers = []
        for (let i = 0; i < docks.length; i++) {
            componentGenerator.addDockerDetails(i, docks[i]);
            dockerManager.activeDockerContainers.push({
                "port": docks[i].port,
                "name": docks[i].name
            });
        }
    },

    sendGet: function (params, restUrl, callback) {

        $.get(buildUrl(dockerManager.url, dockerManager.port, restUrl), params,
            function (returnedData) {
                data = JSON.parse(returnedData);
                callback(data);
            }).fail(function () {
            console.log("error");
        });

    },
    getAllDockers: function () {
        $.ajax({
            crossDomain: true,
            type: "GET",
            url: buildUrl(dockerManager.url, dockerManager.port, "/dockers/details"),
            dataType: 'text'
        }).done(function (jsondata) {
            let data = JSON.parse(jsondata);
            dockerManager.createDockerList(data["message"]);
        })
            .fail(function (jsondata) {
                console.log("Error occured with this data", jsondata)
            });
    },

    // get printer status using the container name
    getDockerStatus: function (containerName) {
        this.sendGet({printerid: containerName}, "/docker/status", function (data) {
            console.log(data);
        });
    },


    stopDocker: function (containerName) {
        this.sendGet({printerid: containerName}, "/docker/stop", function (data) {
            console.log(data);
        });
    },

    startDocker: function (containerName) {
        this.sendGet({printerid: containerName}, "/docker/start", function (data) {
            console.log(data);
        });
    },

    startAllDockers: function (count) {
        this.sendGet({printerCount: count}, "/dockers/start", function (data) {
            console.log(data);
        });
    },

    stopAllDockers: function (count) {
        this.sendGet({printerCount: count}, "/dockers/stop", function (data) {
            console.log(data);
        });
    }
};
