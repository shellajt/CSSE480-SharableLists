var shareableLists = shareableLists || {};

shareableLists.editing = false;

shareableLists.attachEventHandlers = function() {
	$("#insert-task-modal").on("shown.bs.modal", function() {
		$("input[name=name]").focus();
	});
}

shareableLists.enableButtons = function() {
	$("#add-task").click(function() {
		$("#insert-task-modal .modal-title").html("Add a task");
		$("#insert-task-modal button[type=submit]").html("Add task");

		$("#insert-task-modal input[name=name]").val("");

        // TODO: Deal w/ timezones
        var currentDate = new Date();
        console.log(currentDate.toISOString().substring(0, 16));
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
            $("#insert-task-modal input[name=is_complete]").attr('checked', 'checked');
        }
        $("#insert-task-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});

	$(".delete-task").click(function() {
		entityKey = $(this).find(".entity-key").html();

		$("#delete-task-modal input[name=entity_key]").val(entityKey);
	});
}

$(document).ready(function() {
	shareableLists.enableButtons();
	shareableLists.attachEventHandlers();
});
