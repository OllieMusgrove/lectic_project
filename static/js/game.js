// var question_ans = '{{ question_select.answer }}'
// var question_select = '{{ question_select }}';
// var csrf_token = '{{ csrf_token }}';
// var quiz_slug = '{{ question_select.quiz.slug }}';
// var quest_num = '{{ question_number }}';
// var quest_count = '{{ questions.count }}';
// var init_quiz_no = '{{ init_quiz }}';
// var new_quiz = '{{ quiz_attempt.auto_id }}'
// var quest_total = parseInt(quest_count)

var timeRemaining = 10;
console.log("ajax script activated");
console.log("question number = " + quest_num);
$(document).ready(function () {
    console.log("doc ready")
    var timerScript = setInterval(timeLimitProcess, 1000);
    console.log("Timer Started")
    var start = new Date();
    console.log("time = " + start);
    $('#attempt_form').on('submit', function (event) {
        event.preventDefault();
        var end = new Date();
        var difference = (end - start) / 1000;
        console.log("time = " + difference + " seconds");
        // var question_ans = '{{ question_select.answer }}';
        console.log("Answer = " + question_ans)
        // alert("Elasped time = " + difference + " seconds \n Correct Answer = " + question_ans);
        start = new Date();
        $.ajax({
            type: "POST",
            url: "/lectic/" + quiz_slug + "/game/" + quest_num + "/" + init_quiz_no + "/",
            data: {
                'csrfmiddlewaretoken': $('#attempt_form input[name=csrfmiddlewaretoken]').val(),
                'attempt': $('#attempt_text').val(),
                'time': difference,
            },
            success: function (data) {
                var new_num = parseInt(quest_num) + 1
                console.log(new_num)
                if (quest_total > new_num) {
                    // alert("Destination id = {{ quiz_attempt.auto_id }}")
                    location.href = "/lectic/" + quiz_slug + "/game/" + new_num + "/" + new_quiz + "/";
                }
                else {
                    location.href = "/lectic/" + quiz_slug + "/quiz_end/" + new_quiz + "/";
                }
            },
            dataType: 'html'
        });
    });
    function timeLimitProcess() {
        if (timeRemaining == 1) {
            console.log("Time Up!");
            // clearTimeout(timerScript);
            submitProcess();
        } else {
            timeRemaining--;
            console.log(timeRemaining);
        }
    }
    function submitProcess() {
        var end = new Date();
        var difference = (end - start) / 1000;
        console.log("time = " + difference + " seconds");
        // var question_ans = '{{ question_select.answer }}';
        console.log("Answer = " + question_ans)
        // alert("Elasped time = " + difference + " seconds \n Correct Answer = " + question_ans);
        start = new Date();
        $.ajax({
            type: "POST",
            url: "/lectic/" + quiz_slug + "/game/" + quest_num + "/" + init_quiz_no + "/",
            data: {
                'csrfmiddlewaretoken': $('#attempt_form input[name=csrfmiddlewaretoken]').val(),
                'attempt': $('#attempt_text').val(),
                'time': difference,
            },
            success: function (data) {
                var new_num = parseInt(quest_num) + 1
                console.log(new_num)
                if (quest_total > new_num) {
                    // alert("Destination id = {{ quiz_attempt.auto_id }}")
                    location.href = "/lectic/" + quiz_slug + "/game/" + new_num + "/" + new_quiz + "/";
                }
                else {
                    location.href = "/lectic/" + quiz_slug + "/quiz_end/" + new_quiz + "/";
                }
            },
            dataType: 'html'
        });
    }
});
