// GLOBAL VARIABLES
// var question_ans = '{{ question_select.answer }}'
// var question_select = '{{ question_select }}';
// var csrf_token = '{{ csrf_token }}';
// var quiz_slug = '{{ question_select.quiz.slug }}';
// var quest_num = '{{ question_number }}';
// var quest_count = '{{ questions.count }}';
// var init_quiz_no = '{{ init_quiz }}';
// var new_quiz = '{{ quiz_attempt.auto_id }}'
// var quest_total = parseInt(quest_count)

//Script
var timeRemaining = 10;
console.log("ajax script activated");
console.log("question number = " + quest_num);

//When page is loaded...
$(document).ready(function () {
    console.log("doc ready");
    var timerScript = setInterval(timeLimitProcess, 1000);
    console.log("Timer Started");
    var start = new Date();
    console.log("time = " + start);

    //When submit button is pressed
    $('#attempt_form').on('submit', function (event) {
        event.preventDefault();
        var x = false
        submitProcess(x);
    });

    //Called every 1 second
    function timeLimitProcess() {
        if (timeRemaining == 1) {
            console.log("Time Up!");
            // clearTimeout(timerScript);
            var x = true
            submitProcess(x);
        } else {
            timeRemaining--;
            console.log(timeRemaining);
        }
    }

    // Called when timer done or submit button pressed
    function submitProcess(forced) {
        var end = new Date();
        var difference = (end - start) / 1000;
        console.log("time = " + difference + " seconds");
        console.log("Answer = " + question_ans)
        console.log("new message?");
        start = new Date();
        var alertStyle
        var titleMes
        var textMes
        var submittedAns = $('#attempt_text').val();
        var stringSub = String(submittedAns);
        var stringAns = String(question_ans);
        console.log(stringSub);
        console.log(stringAns);
        var lowerSub = stringSub.toLowerCase();
        var lowerAns = stringAns.toLowerCase();
        console.log(lowerSub);
        console.log(lowerAns);
        // var question_ans = question_ans.toLowerCase();
        // console.log("sanity check");
        // console.log("Lower submitted = " + submittedAns);
        // console.log("Lower answer = " + question_ans);
        if (forced) {
            console.log("This was forced")
            alertStyle = "warning"
            titleMes = "Out of time!"
            textMes = "Answer = " + question_ans
        }
        else {
            console.log("This was not forced")
            if (lowerSub === lowerAns) {
                alertStyle = "success"
                titleMes = "Correct!"
                textMes = "Answer = " + question_ans
                console.log("Correct Answer JS")
            }
            else {
                alertStyle = "error"
                titleMes = "Incorrect"
                textMes = "Answer = " + question_ans
                console.log("Incorrect Answer JS")
            }
        }

        //Ajax method to send answer and time back to Django
        $.ajax({
            type: "POST",
            url: "/lectic/" + quiz_slug + "/game/" + quest_num + "/" + init_quiz_no + "/",
            data: {
                'csrfmiddlewaretoken': $('#attempt_form input[name=csrfmiddlewaretoken]').val(),
                'attempt': $('#attempt_text').val(),
                'time': difference,
            },
            //Once posted, this method is called
            success: function (data) {
                console.log("Sumbitted answer = ")
                console.log(submittedAns)
                clearTimeout(timerScript);
                timeLeft = 0;
                //Sweet Alert brings up an animated js alert
                swal(titleMes, textMes, alertStyle)
                    .then(() => {
                        var new_num = parseInt(quest_num) + 1;
                        console.log(new_num)
                        if (quest_total > new_num) {
                            location.href = "/lectic/" + quiz_slug + "/game/" + new_num + "/" + new_quiz + "/";
                        }
                        else {
                            location.href = "/lectic/" + quiz_slug + "/quiz_end/" + new_quiz + "/";
                        }
                    });
            },
            dataType: 'html'
        });
    }
});
