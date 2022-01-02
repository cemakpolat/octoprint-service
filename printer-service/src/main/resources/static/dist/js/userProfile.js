const userProfiler = {
    selectedModelsNames: [],
    dataLoadingFromPrinters: null,
    printableModels: null,
    port: config.port,
    url: config.url,


    updatePreferencesPercentages: function (eco, time, cost) {
        console.log(eco, time, cost);
        this.transmitProfile({eco: eco, time: time, cost: cost});
    },
    sendPost: function (params, restUrl, callback) {
        $.post(buildUrl(userProfiler.url, userProfiler.port, restUrl),
            params,
            function (returnedData) {
                data = JSON.parse(returnedData);
                callback(data);
            }).fail(function () {
            console.log("error");
        });
    },
    transmitProfile: function (profile) {
        this.sendPost(profile, "/user/preferences", function (data) {
            console.log(data);
        });
    }
};