// if new slider is added in home.html then you need to add here as well
$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2] //gives the main object data of the parent node child
    // console.log(id) 
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id: id 
        },
        success: function(data) {
             eml.innerText = data.quantity
             document.getElementById("amount").innerText = data.amount
             document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2] //gives the main object data of the parent node child
    // console.log(id) 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id: id 
        },
        success: function(data) {
             eml.innerText = data.quantity
             document.getElementById("amount").innerText = data.amount
             document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id: id 
        },
        success: function(data) {
            console.log("Delete")
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove() 
            // whole rows of divs are deleted using multiple parent node 5:33:17
        }
    })
})
$('.remove-preorder').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        type:"GET",
        url:"/removepreorder",
        data:{
            prod_id: id 
        },
        success: function(data) {
            console.log("Delete")
            // document.getElementById("amount").innerText = data.amount
            // document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()  
            // window.locate.reload()
            // whole rows of divs are deleted using multiple parent node 5:33:17
        }
    })
})

var stock = document.getElementById("stock").value;
var preOrder = document.querySelector(".preorder");
var addCart = document.querySelector(".addcart"); 
console.log(stock)
console.log("nasdfasdf")

if(stock<1){
    preOrder.classList.remove("d-none");  
    addCart.classList.add('d-none');  
}
else{
    addCart.classList.remove("d-none");
}



// to reduce stock once customer orders the product
// var stock = document.getElementById("stock").value;
