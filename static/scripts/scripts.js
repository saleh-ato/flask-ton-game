const totalSpan = document.getElementById('total');
coin=document.getElementsByClassName('inner-circle')[0]
console.log(coin);
coin.addEventListener("click", animate)
sumvalue=parseInt(totalSpan.textContent);
tapvalue=+1
width=290
function animate(params) {
    // console.log(++num);
    // console.log(coin.offsetWidth);
    // coin.style.width= width*20
    // setTimeout(500)
    // coin.style.width= width*1.5
    // console.log(coin.offsetWidth);
    // var target = Math.random()+0.5; // for testing, give a random value between 0.5 and 1.5
    // document.getElementsByClassName('inner-circle')[0].style.transform = "scale("+target+")";
    // innerCircle.classList.toggle('scale');
}
// const tilt = $('.circle').tilt({
//     maxTilt: 55,
//     scale: 1.05,
//     speed:10000,
// });
document.addEventListener('DOMContentLoaded', function() {
    const innerCircle = document.querySelector('.inner-circle');

    innerCircle.addEventListener('click', function() {
        // Toggle the scale class on click
        innerCircle.classList.toggle('scale');

        // Optionally, you can reset the scale after a delay
        setTimeout(function() {
            innerCircle.classList.remove('scale');
        }, 70); // Time should match the CSS transition duration
    });
});
// _______________
// Adding a click event listener to the coin element
coin.addEventListener('click', function(event) {
    // console.log(++sumvalue);    
    // Create a new div element to display the time
    const timeDisplay = document.createElement('div');
    timeDisplay.className = 'time-display';
    // Get the current time, add 1 hour, and format it to a string
    // const currentTime = new Date();
    // tapvalue = tapvalue;
    // currentTime.setHours(currentTime.getHours() + 1); // Add 1 hour
    // timeDisplay.innerText = currentTime.toLocaleTimeString(); // Format time
    timeDisplay.innerText = "+"+tapvalue;

    total=parseInt(parseInt(totalSpan.textContent.replace(/,/g, ''), 10))+tapvalue
    console.log(total);
    
    //////////// document.getElementById('total').innerText=total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    totalSpan.textContent=total
    formatInnerNumber(totalSpan)

    // Position the element where the user clicked
    timeDisplay.style.position = 'absolute'; // Ensure the element can be positioned absolutely
    timeDisplay.style.left = `${event.pageX}px`;
    timeDisplay.style.top = `${event.pageY}px`;
    timeDisplay.style.opacity = '1'; // Initialize with full opacity

    // Append to the body
    document.body.appendChild(timeDisplay);

    // Set a timeout to fade out the element
    setTimeout(() => {
        timeDisplay.style.transition = 'opacity 0.3s ease'; // Smooth transition for opacity
        timeDisplay.style.opacity = '0'; // Start fade out

        // Delay removing it to allow fade out effect
        setTimeout(() => {
            timeDisplay.remove(); // Remove the element from the DOM
        }, 300); // Delay to wait for fade out
    }, 300); // Time to wait before starting fade-out
});
function formatInnerNumber(element) {
    if (!element || typeof element.innerText !== 'string') {
      console.error('Invalid element provided.');
      return;
    }
    
    // Extract the inner text
    const rawNumber = element.innerText.trim();
  
    // Remove any non-digit characters (optional if your number includes symbols)
    const numericString = rawNumber.replace(/[^0-9.-]/g, '');
  
    // Parse the number
    const number = parseFloat(numericString);
    if (isNaN(number)) {
      console.error('The inner text does not contain a valid number.');
      return;
    }
  
    // Format the number with thousand separators
    const formattedNumber = number.toLocaleString();
  
    // Update the element's inner text
    element.innerText = formattedNumber;
  }
  formatInnerNumber(totalSpan)
//   ____________
const userId = document.getElementById("user-id").getAttribute("data-user"); // دریافت user_id از HTML
coin.addEventListener("click", () => {
    fetch("/click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId })  // آی‌دی کاربر
    })
    .then(response => response.json())
    .then(data => console.log("New balance:", data.balance));
});
