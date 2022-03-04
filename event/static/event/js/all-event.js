///START READY FUNCTION
//Global variable
let search = "";
//TODO: sự kiện trùng với lĩnh vực của tôi, hoặc ngành tôi học,...
$(document).ready(function () {

    //call function init
    initFunction();

    //Call function
    getAllEvent();

    //Call function contest near me
    getAllEventNearMe();
});
///END READY FUNCTION


///START FUNCTION

//Init function
let initFunction = function () {
    //Detect search input enter press
    $("body").delegate("#search-input", "keypress", function (e) {
        if (e.keyCode === 13) {
            search = this.value;
            getAllEvent();
        }
    });
}


//Render all event card
function renderEvent(data) {
    return `<div class="card mx-2 my-2" style="width: 220px;">
               <img class="card-img-top" src="${data['background']}" alt="Card image">
               <div class="card-body">
                   <p class="contest-title">
                       <a href="${data['full_url']}" style="font-size: 14px;">${data['name']}</a>
                   </p>
                   <p>${data['start_date']} - ${data['end_date']}</p>
                   <p>${data['address']}</p>
               </div>
               <div class="card-footer text-center v-detail">
                    <a href="${data['full_url']}" class="text-success">Xem chi tiết</a>
               </div>
           </div>`;
}

//Render all event near me
function renderEventNearMe(idx, data) {
    return `<div class="col-2 pt-2">
                <p>${idx + 1}</p>
            </div>
            <div class="col-10 pt-2">
                <p><a href="${data['full_url']}">${data['name']}</a></p>
                <p>${data['address']}</p>
            </div>`
}

//Call api get all event
let getAllEvent = function () {
    $(".all-event").html("");
    $.ajax({
        url: Urls["event:all-event"](),
        data: {
            "search": search
        },
        statusCode: {
            200: function (data) {
                let content = "";
                $.each(data, function (index, value) {
                    content += renderEvent(value);
                });
                if (data.length <= 0) {
                    content = "<p>Không có cuộc thi nào</p>"
                }
                $(".all-event").html(content);
                $("#result-num").text(`${data.length} kết quả`);
            }
        }
    })
}

//Function call event near me
let getAllEventNearMe = function () {
    $("#id_list_contest_near_me").html("");
    $.ajax({
        url: Urls["event:get-event-near-me"](),
        statusCode: {
            200: function (data) {
                let content = "";
                $.each(data, function (index, value) {
                    content += renderEventNearMe(index, value);
                });
                if (data.length <= 0) {
                    content = "<p>Không có sự kiện nào gần bạn!</p>"
                }
                $("#id_list_event_near_me").html(content);
            }
        }
    })
};