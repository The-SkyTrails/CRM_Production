
// $(document).ready(function(){
// var calendar = $('#calendar').fullCalendar({
//     header: {
//         left: 'prev,next today',
//         center: 'title',
//         right: 'month,agendaWeek,agendaDay'
//     },
//     events:'/Admin/all_appointment/',
//            selectable: true,
//            selectHelper: true,
//            editable: true,
//            eventLimit: true,
//            select: function (start, end, allDay){
//             $('#eventModal').modal('show');
//             $('#saveEventBtn').on('click', function () {
               
//                 var title = $('#eventTitleInput').val();
//                 // var startdateTime = $('#startdate').val();
//                 // var enddateTime = $('#enddate').val();
                
                
//                 $('#eventModal').modal('hide');

//                 if (title) {
                    
//                     var start = $.fullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss");
                   
//                     var end = $.fullCalendar.formatDate(end, "Y-MM-DD HH:mm:ss");
//                     $.ajax({
//                         type: "GET",
//                         url: '/Admin/add_appointment/',
//                         data: {'title': title,'start': start,'end':end},
//                         dataType: "json",
//                         success: function (data) {
//                             calendar.fullCalendar('refetchEvents');
//                             alert("Added Successfully");
//                         },
//                         error: function (data) {
//                             alert('There is a problem!!!');
//                         }
//                     });
//                 }
//             });
//         },
//     });
// });


$(document).ready(function(){
    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: '/Admin/all_appointment/',
        selectable: true,
        selectHelper: true,
        editable: true,
        eventLimit: true,
        select: function (start, end, allDay) {
            $('#eventModal').modal('show');

            $('#saveEventBtn').on('click', function () {
                console.log("workinggggggg")
                var title = $('#eventTitleInput').val();
                console.log("titleee",title)
                var time = $('#eventTime').val();
                console.log("time",time)
                var start = $.fullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss");
                console.log("starttttttt",start)
                console.log("titleee",title)
                console.log("time",time)
                console.log("start",start)
                $('#eventModal').modal('hide');

                if (title) {
                    // var end = $.fullCalendar.formatDate("Y-MM-DD");
                    $.ajax({
                        type: "GET",
                        url: '/Admin/add_appointment/',
                        data: {'title': title, 'start': start,'time':time},
                        dataType: "json",
                        success: function (data) {
                            calendar.fullCalendar('refetchEvents');
                            alert("Added Successfully");
                        },
                        error: function (xhr, status, error) {
                            console.error('Error:', error);
                            alert('There is a problem!!!');
                        }
                    });
                }
            });
        },
    });
});
