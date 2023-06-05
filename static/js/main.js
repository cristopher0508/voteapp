 menu = document.querySelector('.home-ul-responsive');
 boton = document.getElementById('boton')

function mostrar() {
    menu = document.querySelector('.home-ul-responsive');
    if(menu.style.display == 'none'){
        menu.style.display = 'block';
    }
    else{
        menu.style.display = 'none'
    }
}




function AbrirLikes(){
    container_likes = document.getElementById('likes-users')

    if(container_likes.style.display == "none"){
        container_likes.style.display = 'block'
    }
    else{
        container_likes.style.display = "none"
    }
}

container_likes = document.getElementById('likes-users')

button = document.querySelector('.button-x')

boton_two = document.querySelector('.strong-1')


function Cerrar(){
    container_likes = document.getElementById('likes-users')

    if (container_likes.style.display == 'block') {
        container_likes.style.display = 'none'
        
    }

}


