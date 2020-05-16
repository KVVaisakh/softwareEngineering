document.getElementById("createn").addEventListener("click", function(){
    document.querySelector(".popup").style.display = "flex";
})

document.querySelector(".newp").addEventListener("click", function(){
    document.querySelector(".popup").style.display = "none";
})



document.getElementById("v").addEventListener("click", function(){
    document.querySelector(".card__cta").style.display = "none";
    document.querySelector(".viewmembers").style.display = "flex";
})

document.querySelector(".close").addEventListener("click", function(){
    document.querySelector(".card__cta").style.display = "initial";
    document.querySelector(".viewmembers").style.display = "none";
})

document.getElementById("edit").addEventListener("click", function(){
    document.querySelector(".card__cta").style.display = "none";
    document.querySelector(".editmembers").style.display = "flex";
})

document.querySelector(".newc").addEventListener("click", function(){
    document.querySelector(".card__cta").style.display = "initial";
    document.querySelector(".editmembers").style.display = "none";
})