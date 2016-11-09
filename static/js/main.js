var shareableLists = shareableLists || {};

shareableLists.editing = false;
shareableLists.sideNavShown = false;

shareableLists.attachEventHandlers = function() {
    $("#insert-task-modal").on("shown.bs.modal", function() {
        $("input[name=name]").focus();
    });
};

shareableLists.enableButtons = function() {
    // Task buttons
    $("#add-task").click(function() {
        $("#insert-task-modal .modal-title").html("Add a task");
        $("#insert-task-modal button[type=submit]").html("Add task");

        $("#insert-task-modal input[name=name]").val("");

        // TODO: Deal w/ timezones
        var currentDate = new Date();
        // console.log(currentDate.toISOString().substring(0, 16));
        $("#insert-task-modal input[name=due_date_time]").val(currentDate.toISOString().substring(0, 16));
        $("#insert-task-modal input[name=note]").val("");
        $("#insert-task-modal input[name=is_complete]").val(false);
        $("#insert-task-modal input[name=entity_key]").val("").prop("disabled", true);
    });

    $(".edit-task").click(function() {
        $("#insert-task-modal .modal-title").html("Edit this task");
        $("#insert-task-modal button[type=submit]").html("Edit task");

        name = $(this).find(".name").html();
        due_date_time = $(this).find(".due_date_time").html();
        note = $(this).find(".note").html();
        is_complete = $(this).find(".is_complete").html();
        entityKey = $(this).find(".entity-key").html();

        $("#insert-task-modal input[name=name]").val(name);
        var taskDueDate = new Date(due_date_time);
        $("#insert-task-modal input[name=due_date_time]").val(taskDueDate.toISOString().substring(0, 16));
        $("#insert-task-modal input[name=note]").val(note);
        if (is_complete === "True") {
            $("#insert-task-modal input[name=is_complete]").prop('checked', true);
        } else {
            $("#insert-task-modal input[name=is_complete]").prop('checked', false);
        }
        $("#insert-task-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
    });

    $(".delete-task").click(function() {
        entityKey = $(this).find(".entity-key").html();

        $("#delete-task-modal input[name=entity_key]").val(entityKey);
    });

    // List buttons
    $("#add-list").click(function() {
        $("#insert-list-modal .modal-title").html("Add a list");
        $("#insert-list-modal button[type=submit]").html("Add list");

        $("#insert-list-modal input[name=name]").val("");
        $("#name-input").focus();
        $("#insert-list-modal input[name=shared]").val("");
        $("#insert-list-modal input[name=entity_key]").val("").prop("disabled", true);
    });

    $("#edit-list").click(function() {
        $("#insert-list-modal .modal-title").html("Edit this list");
        $("#insert-list-modal button[type=submit]").html("Edit list");

		name = $("#current-list-name").html();
		entityKey = $("#current-list-key").html();
        emailString = $("#current-list-emails").html();

        $("#insert-list-modal input[name=name]").val(name);
        $("#insert-list-modal input[name=shared]").val(emailString);
        $("#insert-list-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
    });

    $("#delete-list").click(function() {
        entityKey = $("#current-list-key").html();

        $("#delete-list-modal input[name=entity_key]").val(entityKey);
    });

    $(".task-completed-checkbox").click(function() {
        var index = $(".task-completed-checkbox").index(this);
        var dataToSend = {
            "index": index,
            "entityKey": $(".checkbox-entity-key").eq(index).text()
        };

        $.post("/togglecomplete", dataToSend).done(function(data) {
            console.log("Successful toggle complete post: " + JSON.stringify(data));
            if (data.is_complete) {
                $(".task-completed-checkbox").eq(data.index).prop("checked", true);
				$(".edit-task .is_complete").eq(data.index).html("True")
            } else if (!data.is_complete) {
                $(".task-completed-checkbox").eq(data.index).prop("checked", false);
				$(".edit-task .is_complete").eq(data.index).html("False");
            }
        }).fail(function(jqxhr, textStatus, error) {
            console.log("POST Request Failed: " + textStatus + ", " + error);
        });
    });

    $(".clickable").click(function() {
    	$('#task-detail-modal').modal('show');

    	name = $(".name").html();
        due_date_time = $(".due_date_time").html();
        note = $(".note").html();
        is_complete = $(".is_complete").html();
        comments = $(".comments").html();
        taskKey = $(".entity-key").html();
        if (comments != null) {
        	stringComments = shareableLists.parseComments(comments);
        } else {
        	stringComments = "";
        }
        
        console.log(name);
        console.log(due_date_time);
        console.log(note);
        console.log(is_complete);
        console.log(comments);
        console.log(taskKey);
        console.log(stringComments);

        $("#task-detail-modal input[name=name]").val(name).prop("readonly", true);
        var taskDueDate = new Date(due_date_time);
        $("#task-detail-modal input[name=due_date_time]").val(taskDueDate.toISOString().substring(0, 16)).prop("readonly", true);
        $("#task-detail-modal input[name=note]").val(note).prop("readonly", true);
        if (is_complete === "True") {
            $("#task-detail-modal input[name=is_complete]").prop('checked', true).prop("disabled", true);
        } else {
            $("#task-detail-modal input[name=is_complete]").prop('checked', false).prop("disabled", true);
        }
        $("#task-detail-modal input[name=task-key]").val(taskKey);
        $("#task-detail-modal #comments-box").val(stringComments).prop("readonly", true);
    });
};

shareableLists.parseComments = function(comments) {
	comments = comments.substr(1, comments.length-2);
	splitArr = comments.split(",");
	commentsArr = [];
	for (var i = 0; i < splitArr.length; i++) {
		currentString = splitArr[i];
		if(i == 0) {
			commentsArr.push(currentString.substr(2, currentString.length-3));
		} else {
			commentsArr.push(currentString.substr(3, currentString.length-4));
		}
	}

	commentString = "";
	for (var j = 0; j < commentsArr.length; j++) {
		commentString += commentsArr[j] + "\n";
	}
	return commentString;
}

function toggleNav() {
    if (!shareableLists.sideNavShown) {
        openNav();
        shareableLists.sideNavShown = true;
    } else {
        closeNav();
        shareableLists.sideNavShown = false;
    }
};

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("sidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
};

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("sidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
};

$(document).ready(function() {
    shareableLists.enableButtons();
    shareableLists.attachEventHandlers();
});
