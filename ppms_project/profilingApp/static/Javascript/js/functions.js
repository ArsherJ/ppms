function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("grid").style.marginLeft = "250px";
    document.getElementById("footer").style.marginLeft = "250px";
    
    document.getElementById('navButton').onclick = closeNav;
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("grid").style.marginLeft = "0";
    document.getElementById("footer").style.marginLeft = "0";
    
    document.getElementById('navButton').onclick = openNav;
}
function openOffcanvas() {
    openNav();
    document.getElementById("myCanvasNav").style.width = "100%";
    document.getElementById("myCanvasNav").style.opacity = "0.95";  
    document.getElementById("mySidenav").style.zIndex = 5;
    document.getElementById('navButton').onclick = closeOffcanvas;
    document.body.style.overflowY="hidden";
}
function closeOffcanvas() {
    closeNav();
    document.getElementById("myCanvasNav").style.width = "0%";
    document.getElementById("myCanvasNav").style.opacity = "0"; 
    document.body.style.backgroundColor = "white";
    document.getElementById('navButton').onclick = openOffcanvas;
    document.body.style.overflowY="visible";
}