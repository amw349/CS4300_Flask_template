// typewriter animation
window.onload = function() {
    document.getElementById("splash-title-animation").className += "line-1 anim-typewriter";
    console.log(window.location)
    window.setTimeout(function(){
      // Move to a new location or you can do something else
      $('#splash-container').addClass('animated fadeOut');
    }, 3000);
    window.setTimeout(function(){
      window.location += 'search';
    }, 4000);
}
