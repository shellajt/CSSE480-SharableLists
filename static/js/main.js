var rh = rh || {};
rh.sl = rh.sl || {};

rh.sl.sideNavShown = false;

$(document).ready(function() {
    console.log("Hello, JavaScript world!");
});

function toggleNav() {
	if (!rh.sl.sideNavShown) {
		openNav();
		rh.sl.sideNavShown = true;
	} else {
		closeNav();
		rh.sl.sideNavShown = false;
	}
}

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}