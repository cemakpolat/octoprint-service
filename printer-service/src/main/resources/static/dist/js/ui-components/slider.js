var startingValues = [33, 66];

$(".slider")
    .slider({
        min: 0,
        max: 100,
        range: true,
        values: startingValues,
        create: function (event, ui) {
            onSlide({
                values: startingValues
            });
        },
        slide: function (event, ui) {
            onSlide(ui);
        },
        change: function (event, ui) {
            updateUserProfileValues(ui);
        }
    });

function onSlide(ui) {
    var totalWidth = $(".slider").width();
    $("#profile_eco").html(ui.values[0]);
    $("#profile_time").html(ui.values[1] - ui.values[0]);
    $("#profile_cost").html(100 - (ui.values[1]));
    $(".left-color").width((ui.values[0]) / 100 * totalWidth);
}

function updateUserProfileValues(ui) {
    var eco = ui.values[0];
    var time = ui.values[1] - ui.values[0];
    var cost = 100 - (ui.values[1]);
    userProfiler.updatePreferencesPercentages(eco, time, cost);
}