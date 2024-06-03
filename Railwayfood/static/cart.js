document.addEventListener('DOMContentLoaded', () =>{
    const addToCartButtons = document.querySelectorAll('.bxs-cart-add');
    const cartItemCount = document.querySelector('.cart-icon span');
    const cartItemsList = document.querySelector('.cart-tems');
    const cartTotal = document.querySelector('.cart-total');
    const cartIcon = document.querySelector('.cart-icon');
    const sidebar= document.getElementById('sidebar');

    let cartItems = [];
    let totalAmount = 0;

    
    addToCartButtons.forEach((button, index)=> {
        button.addEventListener('click', ()=>{
            const item ={
                name: document.querySelectorAll('.card .card--title')[index].textContent,
                price: parseFloat(
                    document.querySelectorAll('.card .card--price .price')[index].textContent.slice(1),
                ),
                quantity: 1,
            };

            const existingItem = cartItems.find(
                (cartItem) => cartItem.name === item.name,
            );
            if (existingItem){
                existingItem.quantity++;
            } else {
                cartItems.push(item);
            }

            totalAmount += item.price;

            updateCartUI();
        });

        function updateCartUI() {
            updateCartItemCount(cartItems.length);
            updateCartItemList();
            updateCartTotal();
        }

        function updateCartItemCount(count) {
            cartItemCount.textContent = count;
        }

        function updateCartItemList() {
            cartItemsList.innerHTML = '';
            cartItems.forEach((item, index) => {
                const cartItem = document.createElement('div');
                cartItem.classList.add('cart-item', 'individual-cart-item');
                cartItem.innerHTML = `
                <span>(${item.quantity}x)${item.name} </span>
                <span class="cart-item-price">RM${(item.price * item.quantity).toFixed(
                    2,
                )}
                <button class="remove-btn" data-index="${index}"><i class='bx bx-x-circle' ></i></button>
                </span>
                `;

                cartItemsList.append(cartItem);
            });
       

            const removeButtons = document.querySelectorAll('.remove-btn');
            removeButtons.forEach((button)=>{
                button.addEventListener('click', (event) => {
                    const index = event.target.dataset.index;
                    removeItemFromCart(index);
                });
            });
        }

        function removeItemFromCart(index){
            const removeItem = cartItems.splice(index, 1)[0];
            totalAmount -= removeItem.price * removeItem.quantity;
            updateCartUI();
        }

        function updateCartTotal (){
            cartTotal.textContent = `RM${totalAmount.toFixed(2)}`;
        }

        const sidebar = document.getElementById('sidebar');
        const cartIcon = document.querySelector('.cart-icon');
        const closeButton = document.querySelector('.sidebar-close');


        function openSidebar() {
        sidebar.classList.add('open');
        }


        function closeSidebar() {
        sidebar.classList.remove('open');
        }


        cartIcon.addEventListener('click', openSidebar);


        closeButton.addEventListener('click', closeSidebar);
      
    });
});