// $(document).ready(() => $("#submitButton").on("click", () => {
//     $.post("api/test", {v: $("#linkField").val()}, function(result){
//         $("#progressModal").modal("show");
//     });
// }));

$(document).ready(main);

let currentCols = 0;

let queueCardTemplate = '<'

function addToQueue()
{
    let cont = $("#videoRows");
    cont.append('<div class="col"><div class="card" style="width: 18rem;"><div class="d-flex justify-content-center"><div class="spinner-border"></div></div><div class="card-body"><h5 class="card-title">Video title</h5><p class="card-text">Video beschreibung</p><a href="#" class="btn btn-danger">Abbrechen</a></div></div></div>');
    currentCols++;
}

function main()
{
    $("#submitButton").on("click", () => {
        $.post("api/test", {v: $("#linkField").val()}, result => {
            addToQueue();
            $("#progressModal").modal("show");

            var interval = setInterval(() => {
                $.get("status/test", (data, stat) => {
                    if(data.status == "finished")
                    {
                        $("#progBar").css("width", 100);
                        clearInterval(interval);
                    }
                    console.log(data.status)
                    $("#progBar").css("width", 300 - data.status * 2);
                });
            }, 100);

        });
    });
}
