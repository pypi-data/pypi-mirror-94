console.log("Input script loaded");

$(document).ready(function () {
    let all_inputs = $(".split-input-group input");
    console.log("Split inputs loaded.")
    if (!window.clear_split_inputs) {
        console.log("Split inputs won't be cleared.")
    } else {
        all_inputs.each(function (count, obj) {
            $(obj).val("");
        })
        console.log("Split inputs have been cleared.")
    }
    all_inputs.keyup(function (e) {
        let target = $(e.target);
        let value = target.val();
        let max_len = target.attr("maxLength");
        if (value.length >= max_len) {
            target.next("input.split-input").focus();
            console.log("Next target selected");
        }
    })
})
