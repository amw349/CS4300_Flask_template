// js method
function showHashtagInfo(tag, button_id) {
    console.log("Got to the actions.js file");
    console.log(button_id);
    var selected_tag_div = document.getElementById(tag);
    var button = document.getElementById(button_id);
    if (selected_tag_div.style.display === "none") {
        selected_tag_div.style.display = "block";
        selected_tag_div.style.backgroundColor = "#5BC0DE";
        selected_tag_div.style.height = "100px";
        button.style.opacity = .7;
    } else {
        selected_tag_div.style.display = "none";
        button.style.backgroundColor = "#5BC0DE";
        button.style.opacity = 1;
    }
}
