window.dash_clientside = Object.assign({}, window.dash_clientside, {
    cursor: {
        update_cursor: function(state) {
            if (state === "busy") {
                document.body.style.cursor = "wait";
            } else {
                document.body.style.cursor = "";
            }
            return state;
        }
    }
});