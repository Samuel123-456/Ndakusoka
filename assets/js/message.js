
let message = document.getElementById('div-message')

let cont = 0

let control = null
function showMessage(params) {
      
      control = setInterval(() => {
            if (cont==3) {
                  message.style.display = 'none'
                  clearInterval(control)
            }
            cont+=1
      }, 1000);
      message.style.display = 'flex'
}

showMessage()  