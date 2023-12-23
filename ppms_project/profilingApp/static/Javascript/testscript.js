$(function () {
  $(document).scroll(function () {
    var $nav = $(".fixed-top");
    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });
});

function openpaneltwo(e) {
  
      // e.preventDefault();
      panelTwo = $('.form-panel.two')[0].scrollHeight;
      $('.form-toggle').addClass('visible');
      $('.form-panel.one').addClass('hidden');
      $('.form-panel.two').addClass('active');
      formHeight.style.minHeight="1150px";
      formHeight.style.maxHeight="1100px";
      $('.form').animate({
        'height': panelTwo
      }, 200);
    };
  


$(document).ready(function() {
    var panelOne = $('.form-panel.one').height(),
      panelTwo = $('.form-panel.two')[0].scrollHeight;
    var formHeight = document.getElementById("formHeight")
    $('.form-panel.two').not('.form-panel.two.active').on('click', function() {
      // e.preventDefault();
      
      $('.form-toggle').addClass('visible');
      $('.form-panel.one').addClass('hidden');
      $('.form-panel.two').addClass('active');
      formHeight.style.minHeight="1150px";
      formHeight.style.maxHeight="2000px";
      $('.form').animate({
        'height': panelTwo
      }, 200);
    });
  
    $('.form-toggle').on('click', function(e) {
      // e.preventDefault();
      $(this).removeClass('visible');
      $('.form-panel.one').removeClass('hidden');
      $('.form-panel.two').removeClass('active');
      formHeight.style.minHeight="500px";
      formHeight.style.maxHeight="500px";
      $('.form').animate({
        'height': panelOne
      }, 200);
    });
  });