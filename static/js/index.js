

container_likes = document.getElementById('likes-users')

if(container_likes){
  
    container_likes.addEventListener('click', ()=>{
    if (container_likes.style.display == 'block') {
        container_likes.style.display = 'none'
        
    }

})

}