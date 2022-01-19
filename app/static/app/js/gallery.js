const cMen = document.querySelector('.men');
const dMen = document.querySelector('.c-men');
const cWomen = document.querySelector('.women');
const dWomen = document.querySelector('.c-women');

cMen.addEventListener('click',()=>{
    dMen.classList.toggle('hide');
    dWomen.classList.add('hide');
})

cWomen.addEventListener('click',()=>{
    dWomen.classList.toggle('hide');
    dMen.classList.add('hide');
})