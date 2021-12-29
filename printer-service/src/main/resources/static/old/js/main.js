$(document).ready(function(){

    $("#btn_print").click(function(){
        doTheThing()
            .then((data) => {
                console.log(data)
                doSomethingElse(data)
            })
            .catch((error) => {
                console.log(error)
            })
    });

    function doSomethingElse(data){
        $("#containers").text(data.id +" "+ data.content);
    }

    function doTheThing() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: 'http://localhost:8080/greetings',
                type: 'GET',
                data: {
                    key: 'value',
                },
                success: function (data) {
                    resolve(data)
                },
                error: function (error) {
                    reject(error)
                },
            })
        })
    }

});
