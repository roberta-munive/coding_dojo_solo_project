// formats the list price in view_property.html with commas and dollar sign
// https://www.geeksforgeeks.org/how-to-format-a-number-as-currency-using-css/

let price_element = document.querySelector(".currency-format");
let price_value = Number(price_element.innerHTML).toLocaleString('en');
price_element.innerHTML = price_value; 
price_element.classList.add("currencySign");

//-------------------------------------------------------------------------------
