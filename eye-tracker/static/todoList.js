const reducer = (state = [], action) => {
    console.log("reducer", state, action);

}
const store = Redux.createStore(reducer);


const content = document.querySelector('#list');
content.innerHTML = "Deployed real-time computer vision stream into a web application"